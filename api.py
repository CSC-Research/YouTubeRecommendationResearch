import argparse
import json
import pymongo
import datetime

# repeat videos - do not repeat videos in DB

try:
    import queue
except ImportError:
    import Queue as queue
	
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

DEVELOPER_KEY = 'AIzaSyB_V6J8JnB-HZ01CwflEtrcDfjqJQtqurg'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
BASE_VIDEO_ID = "1rQ_mphb7HU"

YOUTUBE = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
CLIENT = pymongo.MongoClient("mongodb://py-user:pyuser1@cluster0-shard-00-00-gm9y9.mongodb.net:27017,cluster0-shard-00-01-gm9y9.mongodb.net:27017,cluster0-shard-00-02-gm9y9.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
DB = CLIENT['Cluster0']
COL = DB['posts']

NUM_VIDS = 40

q = queue.Queue()

class Video:
	def __init__(self, videoID, data, flag):

		if flag == 0:
			vidInfo = vid_info_request(videoID)

			self.id = vidInfo[0]
			self.title = vidInfo[1]
			self.description = vidInfo[2]
			self.channelID = vidInfo[3]
			self.tags = vidInfo[4]
			self.categoryID = vidInfo[5]
			self.recs = fill_recs(self.id)

			try:
				self.comments = fill_comments(self.id)
			except:
				self.comments = []	

		elif flag == 1:	
			self.id = data["id"]
			self.title = data["title"]
			self.description = data["description"]
			self.channelID = data["channelID"]
			self.tags = data["tags"]
			self.categoryID = data["categoryID"]
			self.recs = data["recs"]	


	def toString(self):
		rec_list = [x[0] for x in self.recs]
		return "_______________________________________________\n\nTITLE\n" + self.title + "\n\nDESCRIPTION\n" + self.description + "\n\nCHANNEL\n" + self.channelID + "\n\nTAGS\n" + "[" + ",".join(self.tags) + "]" + "\n\nCATEGORY ID\n" + self.categoryID + "\n\nRECOMMENDED VIDEO IDS\n" + "[" + ",".join(rec_list) + "]\n_______________________________________________"

def vid_info_request(videoID):

	print("Getting vid info for ID ")
	print(videoID)
	print("\n")

	vidInfo = []

	try:
		request = YOUTUBE.videos().list(
			part="snippet",
			id=videoID
		)
		response = request.execute()
	except:
		print("API quota exceeded on vid_info_request")
		addVideoToTopOfQueue(videoID)


	vidInfo.append(videoID)
	vidInfo.append(response["items"][0]["snippet"]["title"])
	vidInfo.append(response["items"][0]["snippet"]["description"])
	vidInfo.append(response["items"][0]["snippet"]["channelTitle"])

	try:
		vidInfo.append(response["items"][0]["snippet"]["tags"])
	except:
		vidInfo.append([])

	vidInfo.append(response["items"][0]["snippet"]["categoryId"])

	return vidInfo

def vidToJSON(vid):
	return {
	     "id": vid.id,
		 "title": vid.title,
         "description": vid.description,
		 "channelID" : vid.channelID,
         "tags": vid.tags,
		 "categoryID" : vid.categoryID,
		 "recs" : vid.recs,
		 "comments" : vid.comments,
         }

def vidToJSON_forDB(vid):
	return {
	     "id": vid.id,
		 "title": vid.title,
         "description": vid.description,
		 "channelID" : vid.channelID,
         "tags": vid.tags,
		 "categoryID" : vid.categoryID,
		 "recs" : vid.recs,
		 "comments" : vid.comments,
		 "date" : datetime.datetime.utcnow()
         }

def insertVideotoDB(vid):
	posts = DB.posts

	try:
		return posts.insert_one(vidToJSON_forDB(vid)).inserted_id
	except:
		print("Error when inserting to DB (insertVideotoDB)")
		addVideoToTopOfQueue(vid.id)


def fill_recs(parentID):
	i = 0
	NUM_REC_VIDS = 4
	recs = []
	response = recs_request(parentID)

	for i in range(NUM_REC_VIDS):
		recs.append((parentID, response['items'][i]['id']['videoId']))

	return recs

def recs_request(videoID):
	try:
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
	except:
		print("API quota exceeded on recs_request")
		addVideoToTopOfQueue(videoID)

def fill_comments(videoID):
	cmts = []
	response = comments_request(videoID)

	for part in response["items"]:
		try:
			cmts.append(part["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
		except:
			cmts.append([])

	return cmts

def addVideoToTopOfQueue(videoID):
	q2 = queue.Queue()
	q2.put(videoID)

	for item in q:
		q2.put(item)
		
	queueToFile(q2)

def comments_request(videoID):

	request = YOUTUBE.commentThreads().list(
		part="snippet,replies",
		order="relevance",
		videoId=videoID
	)
	response = request.execute()

	print("here is the resp")
	print(response)

	if(response["error"]["errors"][0]["domain"] == "usageLimits"):
		print("API quota exceeded on comments_request")
		addVideoToTopOfQueue(videoID)
	else:
		print("Video " + videoID + " has no comments")


def get_video_info_and_add_to_DB(videoID):
	v1 = Video(videoID, [], 0)
	v1Info = v1.toString()
	print(insertVideotoDB(v1))
	return v1

def level_order_traversal(videoID):
	count = 10000

	fileToQueue(q)
	
	# q.put(videoID)

	while(count > 0):
		parentID = q.get()

		myquery = {"id": parentID}
		mydoc = COL.find(myquery)

		if(mydoc.count() == 0):
			parentVid = get_video_info_and_add_to_DB(parentID)
			print('Removed parent from q')
			childrenList = parentVid.recs

			for child in childrenList:
				q.put(child[1])	
				print('Added child to q')
				print(child[1])
				print("\n\n")


def queueToFile(q):
	while(True):
		try:
			vid = q.get_nowait()
			
			jsonVid = vidToJSON(vid)
			with open('queue.json', 'w') as fp:
				json.dump(jsonVid, fp, indent=2, separators=(',', ': '))
		except:
			break

def fileToQueue(q):
	with open('queue.json', 'r') as fp:
		try:
			data = json.load(fp)
		except:
			return q
		print(data)
		for video in data:
			q.put(Video("fake", data, 1))
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--qw', help='Search term', default='Google')
	parser.add_argument('--max-results', help='Max results', default=25)
	args = parser.parse_args()

	try:
		# level_order_traversal("1rQ_mphb7HU")
		val = comments_request("PLcE5xa4MnI")
		print(val)
	except HttpError, e:
		print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
