import argparse
import json
import pymongo
import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

DEVELOPER_KEY = 'AIzaSyDpzCbGo6uh952cwFykYKDzwJ4gBMuG4pM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
BASE_VIDEO_ID = "pzjnJjsjSIo"

YOUTUBE = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
CLIENT = pymongo.MongoClient("mongodb://py-user:pyuser1@cluster0-shard-00-00-gm9y9.mongodb.net:27017,cluster0-shard-00-01-gm9y9.mongodb.net:27017,cluster0-shard-00-02-gm9y9.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
DB = CLIENT['Cluster0']

class Video:
	def __init__(self,videoID):

		vidInfo = vid_info_request(videoID)

		self.id = vidInfo[0]
		self.title = vidInfo[1]
		self.description = vidInfo[2]
		self.channelID = vidInfo[3]
		self.tags = vidInfo[4]
		self.categoryID = vidInfo[5]
		self.recs = fill_recs(self.id)
		self.comments = fill_comments(self.id)


	def toString(self):
		rec_list = [x[0] for x in self.recs]
		return "_______________________________________________\n\nTITLE\n" + self.title + "\n\nDESCRIPTION\n" + self.description + "\n\nCHANNEL\n" + self.channelID + "\n\nTAGS\n" + "[" + ",".join(self.tags) + "]" + "\n\nCATEGORY ID\n" + self.categoryID + "\n\nRECOMMENDED VIDEO IDS\n" + "[" + ",".join(rec_list) + "]\n_______________________________________________"

def insertVideotoDB(vid):

	post = {"title": vid.title,
         "description": vid.description,
		 "channelID" : vid.channelID,
         "tags": vid.tags,
		 "categoryID" : vid.categoryID,
		 "recs" : vid.recs,
		 "comments" : vid.comments,
         "date": datetime.datetime.utcnow()}

	posts = DB.posts
	return posts.insert_one(post).inserted_id


def fill_recs(parentID):
	i = 0
	NUM_REC_VIDS = 4
	recs = []
	response = recs_request(parentID)

	for i in range(NUM_REC_VIDS):
		recs.append((parentID, response['items'][i]['id']['videoId']))

	return recs

def recs_request(videoID):
	request = YOUTUBE.search().list(
		part="id,snippet",
		maxResults=30,
		order="relevance",
		q="",
		relatedToVideoId=videoID,
		safeSearch="none",
		type="video"
	)

	return request.execute()

def fill_comments(videoID):
	cmts = []
	response = comments_request(videoID)

	for part in response["items"]:
		cmts.append(part["snippet"]["topLevelComment"]["snippet"]["textOriginal"])

	return cmts


def comments_request(videoID):
	request = YOUTUBE.commentThreads().list(
        part="snippet,replies",
		order="relevance",
        videoId=videoID
    )
	return request.execute()

def vid_info_request(videoID):

	vidInfo = []

	request = YOUTUBE.videos().list(
        part="snippet",
        id=videoID
    )
	response = request.execute()

	vidInfo.append(videoID)
	vidInfo.append(response["items"][0]["snippet"]["title"])
	vidInfo.append(response["items"][0]["snippet"]["description"])
	vidInfo.append(response["items"][0]["snippet"]["channelTitle"])
	vidInfo.append(response["items"][0]["snippet"]["tags"])
	vidInfo.append(response["items"][0]["snippet"]["categoryId"])

	return vidInfo

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--qw', help='Search term', default='Google')
	parser.add_argument('--max-results', help='Max results', default=25)
	args = parser.parse_args()

	# CLIENT.list_database_names()

	try:
		v1 = Video(BASE_VIDEO_ID)
		v1Info = v1.toString()

		print(insertVideotoDB(v1))

		with open('output.txt', 'w') as fp:
			fp.write(v1Info.encode('utf8'))
			
	except HttpError, e:
		print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
