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
		return self.title + " by " + self.channelID
