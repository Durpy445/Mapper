import json
with open('Data.json', 'r') as file:
    data = json.load(file)

Max = 100
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


print(List)

import networkx as nx
G = nx.Graph()


for i in List:
    G.add_node(i[0])

import matplotlib.pyplot as plt 

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

plt.show()