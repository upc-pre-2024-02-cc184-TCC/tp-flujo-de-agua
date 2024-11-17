import csv
import networkx as nx
import plotly.graph_objects as go
import random

# Crear el grafo
G = nx.DiGraph()

def load_graph_from_csv(file_path):
    global G
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            source = row['Source Node'].strip()
            destination = row['Destination Node'].strip()
            flow_capacity = float(row['Flow Capacity']) if row['Flow Capacity'] else 0
            distance = float(row['Distance Between Nodes']) if row['Distance Between Nodes'] else 0
            G.add_edge(source, destination, flow_capacity=flow_capacity, distance=distance)

    return G

def style_water_network_graph():
    """
    Genera un gráfico estilizado del grafo como red de agua potable con nodos y aristas en colores verde y azul pastel.
    """
    # Usamos un layout de distribución eficiente para grafos grandes
    pos = nx.fruchterman_reingold_layout(G)  # Distribución eficiente para grafos grandes

    # Aristas
    edge_traces = []

    for edge in G.edges(data=True):
        src, dst, data = edge
        x0, y0 = pos[src]
        x1, y1 = pos[dst]

        # Color basado en la distancia, en tonos de verde y azul pastel
        edge_color = f"rgba({random.randint(100, 150)}, {random.randint(200, 255)}, {random.randint(200, 255)}, 0.8)"
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            line=dict(width=1, color=edge_color),  # Ancho de línea reducido
            hoverinfo='text',
            text=f"De {src} a {dst}<br>Capacidad: {data['flow_capacity']} L/s<br>Distancia: {data['distance']} km",
            mode='lines'
        )
        edge_traces.append(edge_trace)

    # Nodos
    node_x = []
    node_y = []
    node_colors = []
    node_text = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        # Información sobre el nodo
        connected_edges = list(G.edges(node, data=True))
        total_distance = sum(edge[2]['distance'] for edge in connected_edges)  # Sumar las distancias de las aristas conectadas
        if connected_edges:
            capacities = [edge[2]['flow_capacity'] for edge in connected_edges]
            max_capacity = max(capacities)
            node_text.append(
                f"Estación: {node}<br>Capacidad máxima: {max_capacity} L/s<br>Conexiones: {len(connected_edges)}<br>Distancia total: {total_distance} km"
            )
        else:
            node_text.append(f"Estación: {node}<br>Sin conexiones<br>Distancia total: {total_distance} km")

        # Color de nodos en verde o azul pastel
        node_colors.append(f"rgba({random.randint(100, 150)}, {random.randint(200, 255)}, {random.randint(150, 255)}, 0.8)")  # Verde y azul pastel

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        text=node_text,
        hoverinfo='text',  # Información detallada sobre el nodo
        marker=dict(
            size=5,  # Tamaño reducido para todos los nodos
            color=node_colors,
            line=dict(width=1, color='rgba(80, 80, 80, 0.6)')
        )
    )

    # Crear figura
    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        title="Red de Agua Potable",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        plot_bgcolor='white',
        font=dict(family="Arial", size=12, color="#4A4A4A"),
    )
    return fig

# Código principal para pruebas
if __name__ == "__main__":
    load_graph_from_csv('nodos_conectividad_3.csv')
    print(f"El grafo tiene {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas.")
    fig = style_water_network_graph()
    fig.show()