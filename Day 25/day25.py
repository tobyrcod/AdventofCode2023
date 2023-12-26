import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

with open('input.txt', 'r') as file:
    lines = file.read().rsplit('\n')

def plot_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black',
            font_size=8)

    plt.show()

adjacency_dict = {node: edges.split() for line in lines for node, edges in [line.split(': ')]}
graph = nx.Graph(adjacency_dict)

min_edge_cut = nx.minimum_edge_cut(graph)
graph.remove_edges_from(min_edge_cut)

connected_components = nx.connected_components(graph)
sizes = [len(component) for component in connected_components]
product = np.product(sizes)
print(product, sizes)

