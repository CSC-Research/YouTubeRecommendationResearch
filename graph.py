import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
G = nx.DiGraph()

G.add_node("ROOT")

for i in range(5):
    G.add_node("Child_%i" % i)
    G.add_node("Grandchild_%i" % i)
    G.add_node("Greatgrandchild_%i" % i)

    G.add_edge("ROOT", "Child_%i" % i)
    G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
    G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"
write_dot(G,'test.dot')

# same layout using matplotlib with no labels
plt.title('draw_networkx')
pos =graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=False, arrows=True)
plt.savefig('nx_test.png')

# import networkx as nx
# import matplotlib.pyplot as plt

# DG = nx.DiGraph()
# DG.add_weighted_edges_from([(1, 2, 1), (1, 3, 1), (1, 4, 1), (1, 5, 1)])
# DG.add_weighted_edges_from([(2, 6, 1), (2, 7, 1), (2, 8, 1), (2, 9, 1)])
# DG.add_weighted_edges_from([(6, 10, 1), (10, 11, 1), (11,12, 1), (12, 13, 1)])

# plt.subplot(111)
# pos = nx.tree_layout(DG) 
# nx.draw(DG, pos, with_labels=True, font_weight='bold')
# plt.show()

# # G.add_node("1ne")
# # G.add_node("2wo")
# # G.add_edge("1ne","2wo")

# # plt.subplot(221)
# # nx.draw(G, with_labels=True, font_weight='bold')
# # plt.show()