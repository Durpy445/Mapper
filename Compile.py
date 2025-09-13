import json

from networkx.drawing.nx_pylab import draw_networkx_labels

with open('Data.json', 'r') as file:
    data = json.load(file)

Max = 1000
from unicodedata import name
Names = 10
Amount = {}

def Add(Website):
    if Website not in Amount:
        Amount[Website] = 1
    else:
        Amount[Website] += 1


for Parent in data:
    Add(Parent)
    for Web in data[Parent]:
        Add(Web)



TopSites = sorted(Amount.items(), key=lambda x: (-x[1], x[0]))
List = [site for site, i in TopSites[:Max]]


import networkx as nx
G = nx.Graph()

Sizes = []
Colors = []

Count = 0
for site in List:
    G.add_node(site)



    if site in data:
        for Connection in data[site]:
            if Connection in List and site != Connection:
                G.add_edge(site,Connection)
    else:
        for Parent in data:
            for Connection in data[Parent]:
                if Connection == site and G.has_node(Parent):
                    G.add_edge(Parent,site)


Sizes = [G.degree(node) * 5 for node in G.nodes()]
Colors = [[Amount[node] / Amount[List[0]], 0, 0] for node in G.nodes()]
top_nodes = sorted(G.nodes(), key=lambda n: G.degree(n), reverse=True)[:Names]
labels = {node: node for node in top_nodes}



import matplotlib.pyplot as plt

pos = nx.spring_layout(G)



plt.figure(figsize=(12, 12))
plt.gca().set_facecolor("black")
nx.draw_networkx_labels(G, pos, labels=labels, font_color="white")
nx.draw_networkx_nodes(G, pos, node_size=Sizes, node_color=Colors)

nx.draw_networkx_edges(G, pos, edge_color="gray")

plt.show()
