import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos)
    
    edge_labels = nx.get_edge_attributes(G, 'predicate')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Knowledge Graph Visualization")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
