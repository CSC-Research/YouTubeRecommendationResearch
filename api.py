# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import argparse
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

DEVELOPER_KEY = 'AIzaSyDpzCbGo6uh952cwFykYKDzwJ4gBMuG4pM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(options):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	developerKey=DEVELOPER_KEY)

	request = youtube.search().list(
		part="id,snippet",
		maxResults=30,
		order="relevance",
		q="dogs",
		relatedToVideoId="pzjnJjsjSIo",
		safeSearch="none",
		type="video"
	)
	response = request.execute()

	print(response)
	print(type(response))

	with open('output.json', 'w') as fp:
		json.dump(response, fp, indent=2, separators=(',', ': '))

	print(response)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--q', help='Search term', default='Google')
	parser.add_argument('--max-results', help='Max results', default=25)
	args = parser.parse_args()

	try:
		youtube_search(args)
	except HttpError, e:
		print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
