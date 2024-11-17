import csv
import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo vacío
G = nx.DiGraph()

# Leer el archivo CSV
with open('nodos_conectividad.csv', 'r') as file:
    reader = csv.DictReader(file)
    # Print column names to verify
    print("Column names:", reader.fieldnames)
    for row in reader:
        source = row['Source Node'].strip()
        destination = row['Destination Node'].strip()
        flow_capacity = float(row['Flow Capacity (L/s)']) if 'Flow Capacity (L/s)' in row and row['Flow Capacity (L/s)'] else 0
        distance = float(row['Distance Between Nodes (km)']) if 'Distance Between Nodes (km)' in row and row['Distance Between Nodes (km)'] else 0
        G.add_edge(source, destination, flow_capacity=flow_capacity, distance=distance)

# Ajustar la visualización
plt.figure(figsize=(12, 10))
pos = nx.spring_layout(G, seed=42)  # Posicionamiento estable

# Categorizar nodos según el nombre
node_colors = []
node_sizes = []
for node in G.nodes():
    if "PTAP" in node:  # Plantas de Tratamiento
        node_colors.append('skyblue')
        node_sizes.append(1000)
    elif "Reservorio" in node:
        node_colors.append('green')
        node_sizes.append(800)
    elif "Estación" in node:
        node_colors.append('orange')
        node_sizes.append(700)
    else:  # Hogares u otros
        node_colors.append('lightgray')
        node_sizes.append(500)

# Colores para las aristas según el flujo de capacidad
edge_colors = []
for u, v, d in G.edges(data=True):
    if d['flow_capacity'] > 50:
        edge_colors.append('darkblue')
    elif d['flow_capacity'] > 20:
        edge_colors.append('blue')
    else:
        edge_colors.append('lightblue')

# Dibujar los nodos
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, edgecolors='black')

# Dibujar las aristas con colores según el flujo
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=15, edge_color=edge_colors, width=2)

# Dibujar las etiquetas de los nodos
nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', font_weight='bold')

# Dibujar las etiquetas de las aristas (flujo de capacidad y distancia)
edge_labels = {(u, v): f"{d['flow_capacity']} L/s\n{d['distance']} km" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, font_color='darkred')

# Personalizar la visualización
plt.title("Red de Agua Potable", fontsize=16, fontweight='bold', color='navy')
plt.gca().set_facecolor('whitesmoke')
plt.axis('off')

# Mostrar el grafo
plt.show()