# bellman_ford.py
import networkx as nx

def apply_bellman_ford(G, source, target):
    try:
        # Calculate shortest paths using Bellman-Ford algorithm
        length, path = nx.single_source_bellman_ford(G, source, weight='distance')
        return length[target], path[target]
    except nx.NetworkXNoPath:
        # Return infinity and an empty path if no path exists
        return float('inf'), []
    
    
    
    
    
    