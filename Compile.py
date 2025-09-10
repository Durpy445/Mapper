import json
import math
with open('Data.json', 'r') as file:
    data = json.load(file)

Max = 1000
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


#print(List)

import networkx as nx
G = nx.Graph()

Sizes = []
Colors = []
for site in List:
    G.add_node(site)
    Sizes.append(Amount[site] ^ 4)
    #print(Amount[site])
    Colors.append([Amount[site]/Amount[List[0]],0,0])

    if site in data:
        for Connection in data[site]:
            if Connection in List and site != Connection:
                G.add_edge(site,Connection)
    else:
        for Parent in data:
            for Connection in data[Parent]:
                if Connection == site and G.has_node(Parent):
                    G.add_edge(Parent,site)





import matplotlib.pyplot as plt 

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, node_size = Sizes , node_color=Colors)

plt.show()