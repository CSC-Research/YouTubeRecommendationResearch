import pymongo

CLIENT = pymongo.MongoClient("mongodb://py-user:pyuser1@cluster0-shard-00-00-gm9y9.mongodb.net:27017,cluster0-shard-00-01-gm9y9.mongodb.net:27017,cluster0-shard-00-02-gm9y9.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
DB = CLIENT['Cluster0']
COL = DB['posts']

# querying specific video ID
# myquery = {"id": "Y2d2HLdBF88"}
# mydoc = COL.find(myquery)
# print(mydoc.count())

# querying latest record
# mydoc = COL.find().sort([('date', -1)]).limit(1)

# cquery all
mydoc = COL.find().sort("date")
print(mydoc.count())

for x in mydoc:
  # print("\n")
  # print(x["id"])
  # print(x["title"])
  # print(x["description"])
  # print("_________________________________________")

  vidStr = "\n" + (x["id"]) + "\n" + (x["title"]) + "\n" + (x["channelID"]) + "\n" + "______________________________________________"

  with open('db.txt', 'a') as fp:
				fp.write(vidStr.encode('utf8'))

# counting virus-related entries
# mydoc = COL.find().sort("date")
# print(mydoc.count())

# count = 0
# for x in mydoc:
#   desc = x["description"].lower()
#   if ("coronavirus" in desc) or ("covid" in desc):
#     print(x["id"])
#     count += 1

# print(count)


