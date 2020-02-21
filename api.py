import argparse
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

DEVELOPER_KEY = 'AIzaSyDpzCbGo6uh952cwFykYKDzwJ4gBMuG4pM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
BASE_VIDEO_ID = "pzjnJjsjSIo"

YOUTUBE = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

class Video:
	def __init__(self,videoID):

		vidInfo = vidInfoRequest(videoID)

		self.id = vidInfo[0]
		self.title = vidInfo[1]
		self.description = vidInfo[2]
		self.channelID = vidInfo[3]
		self.tags = vidInfo[4]
		self.categoryId = vidInfo[5]
		self.recs = fill_recs(self.id)
		self.comments = fill_comments(self.id)
		self.ranking = -1


	def toString(self):
		return "_______________________________________________\n\nTITLE\n" + self.title + "\n\nDESCRIPTION\n" + self.description + "\n\nCHANNEL\n" + self.channelID + "\n\nTAGS\n" + "[" + ",".join(self.tags) + "]" + "\n\nCATEGORY ID\n" + self.categoryId + "\n\nRECOMMENDED VIDEO IDS\n" + "[" + ",".join(self.recs) + "]\n_______________________________________________"


def fill_recs(videoID):
	i = 0
	NUM_REC_VIDS = 4
	recs = []
	response = recsRequest(videoID)

	for i in range(NUM_REC_VIDS):
		recs.append(response['items'][i]['id']['videoId'])

	return recs

def recsRequest(videoID):
	request = YOUTUBE.search().list(
		part="id,snippet",
		maxResults=30,
		order="relevance",
		q="dogs",
		relatedToVideoId=videoID,
		safeSearch="none",
		type="video"
	)

	return request.execute()

def fill_comments(videoID):
	cmts = []
	response = commentsRequest(videoID)

	for part in response["items"]:
		cmts.append(part["snippet"]["topLevelComment"]["snippet"]["textOriginal"])

	return cmts


def commentsRequest(videoID):
	request = YOUTUBE.commentThreads().list(
        part="snippet,replies",
		order="relevance",
        videoId=videoID
    )
	return request.execute()

def vidInfoRequest(videoID):

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

	try:
		# videoArr = vidInfoRequest(BASE_VIDEO_ID)
		v1 = Video(BASE_VIDEO_ID)
		v1Info = v1.toString()

		with open('output.txt', 'w') as fp:
			fp.write(v1Info.encode('utf8'))

	except HttpError, e:
		print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
