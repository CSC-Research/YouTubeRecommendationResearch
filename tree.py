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

pp = pprint.PrettyPrinter(indent=4)

rootVid = COL.find_one()
# pp.pprint(rootVid)

rootVidObj = Video('null', rootVid, 1)
print(rootVidObj.toString())


a = Node("a")
b = Node("b", parent=a)
b2 = Node("b2", parent=a)
c2 = Node("c2", parent=b2)
d2 = Node("d2", parent=b2)
c = Node("c", parent=b)
d = Node("d", parent=b)
e = Node(3, parent=d)
f = Node(Simple(3, 'hello').toString(), parent=e)
g = Node(rootVidObj.toString(), parent=f)


DotExporter(a).to_picture("a.png")

def level_order_traversal(g, rootVid):
	
    children = rootVid.children
    for child in children:
        childDB = getChildInfoFromDB()
        childVid = Video(childDB)
        h = Node(childVid.toString(), parent=g)
        level_order_traversal(h, childVid)

        





