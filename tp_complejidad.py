import csv
import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo vacío
G = nx.DiGraph()

# Leer el archivo CSV
with open('nodos_conectividad.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        source = row['Source Node'].strip()
        destination = row['Destination Node'].strip()
        flow_capacity = float(row['Flow Capacity (L/s)']
                              ) if row['Flow Capacity (L/s)'] else 0
        distance = float(row['Distance Between Nodes (km)']
                         ) if row['Distance Between Nodes (km)'] else 0
        G.add_edge(source, destination, flow_capacity=flow_capacity, distance=distance)

# Ajustar la visualización
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)

# Dibujar los nodos
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

# Dibujar las aristas
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')

# Dibujar las etiquetas de los nodos
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

# Dibujar las etiquetas de las aristas (flujo de capacidad y distancia)
edge_labels = {(u, v): f"{d['flow_capacity']} L/s, {d['distance']} km" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Mostrar el grafo
plt.title("Grafo de Nodos y Conectividad")
plt.axis('off')
plt.show()
