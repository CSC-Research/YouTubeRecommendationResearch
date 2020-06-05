from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import pymongo
import pprint
from video import Video

class Simple:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def toString(self):
        return "a: " + str(self.a) + ", b: " + self.b




CLIENT = pymongo.MongoClient("mongodb://py-user:pyuser1@cluster0-shard-00-00-gm9y9.mongodb.net:27017,cluster0-shard-00-01-gm9y9.mongodb.net:27017,cluster0-shard-00-02-gm9y9.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
DB = CLIENT['ReSeed']
COL = DB['posts']

count = 0
l = []
def recurse(vid, parent):
    global count
    global l

    # if count > 150:
    #     print("big count")
    #     return None

    # print("hello\n")
    # print(vid.toString())

    # print("count = ", count)

    l.append(vid.id)

    vidNode = Node(vid.toString(), parent=parent)
    count+=1

    children = vid.recs

    # print(children)

    for child in children:

        # ['parentID', 'childID']
        # ['red', 'green']
        # red, green -> oh fuck thats already in the dict
        # search db again to find something thats red and NOT GREEN

        childID = child[1]
        # print(childID)

        childDBentry = COL.find_one({"id": childID})
        # print(childDBentry)

        if childDBentry != None:
            childVideoObj = Video('null', childDBentry, 1)
                    
            if childID not in l:
                recurse(childVideoObj, vidNode)
            else:
                count += 0

        # here we can check what the child video is
        # we can check if the child video is a video already in the graph (using a list)
        # oh shit, this child is actually already in the graph

        # solutions
        # skip the branch





pp = pprint.PrettyPrinter(indent=4)

rootVid = COL.find_one()
# pp.pprint(rootVid)

a = Node("a")
# b = Node("b", parent=a)
# b2 = Node("b2", parent=a)
# c2 = Node("c2", parent=b2)
# d2 = Node("d2", parent=b2)
# c = Node("c", parent=b)
# d = Node("d", parent=b)
# e = Node(3, parent=d)
# f = Node(Simple(3, 'hello').toString(), parent=e)
# g = Node(rootVidObj.toString(), parent=f)


rootVidObj = Video('null', rootVid, 1)
rootChildren = rootVidObj.recs
recurse(rootVidObj, a)
DotExporter(a).to_picture("d.png")





        





