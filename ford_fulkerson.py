# ford_fulkerson.py
import networkx as nx

def apply_ford_fulkerson(G, source, target):
    try:
        # Calculate maximum flow using Ford-Fulkerson algorithm
        flow_value, flow_dict = nx.maximum_flow(G, source, target, capacity='flow_capacity')
        return flow_value, flow_dict
    except nx.NetworkXError as e:
        # Return zero flow and an empty dictionary if an error occurs
        return 0, {}
    
    
    
    
    