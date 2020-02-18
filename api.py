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
	def __init__(self,vidInfo):
		self.id = vidInfo[0]
		self.title = vidInfo[1]
		self.description = vidInfo[2]
		self.channelID = vidInfo[3]
		self.tags = vidInfo[4]
		self.categoryId = vidInfo[5]
		self.recs = fill_recs(self.id)

	def toString(self):
		return self.title + "\n" + self.description + "\n" + self.channelID + "\n" + "[" + ",".join(self.tags) + "]\n" + self.categoryId + "\n" + "[" + ",".join(self.recs) + "]\n"


def fill_recs(videoID):
    recs = []
    response = recsRequest(videoID)

    for part in response["items"]:
       recs.append(part["id"]["videoId"])

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
		videoArr = vidInfoRequest(BASE_VIDEO_ID)
		v1 = Video(videoArr)
		print(v1.toString())
	except HttpError, e:
		print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
