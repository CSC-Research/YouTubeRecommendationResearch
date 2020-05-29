import igraph
from igraph import Graph, EdgeSeq
import plotly.graph_objects as go

g = Graph()
g.add_vertices(3)
g.add_edges([(0,1), (1,2)])
print(g)