import json
with open('Data.json', 'r') as file:
    data = json.load(file)

import networkx as nx
G = nx.Graph()


for i in data:
    G.add_node(i)

import matplotlib.pyplot as plt 

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)

plt.show()