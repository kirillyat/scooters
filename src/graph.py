import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_nodes_from(range(1, 6))

plt.figure(figsize=(6, 4))
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold')
plt.savefig("graph_1.png", transparent=True)

for i in range(1, 6):
    for j in range(i + 1, 6):
        G.add_edge(i, j, weight=10)

plt.figure(figsize=(6, 4))
pos = nx.circular_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): 10 for i, j in G.edges}, label_pos=0.5, font_weight='bold')
plt.savefig("graph_2.png", transparent=True)

path = [1, 3, 2, 4, 5, 1]

plt.figure(figsize=(6, 4))
H = G.edge_subgraph([(path[i], path[i + 1]) for i in range(len(path) - 1)])
pos = nx.circular_layout(G)
nx.draw(H, pos, with_labels=True, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): 10 for i, j in G.edges}, label_pos=0.5, font_weight='bold')
plt.savefig("graph_3.png", transparent=True)

plt.show()