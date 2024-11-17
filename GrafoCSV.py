import csv
import networkx as nx
import plotly.graph_objects as go

# Crear el grafo
G = nx.DiGraph()


def load_graph_from_csv(file_path):
    global G
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            source = row['Source Node'].strip()
            destination = row['Destination Node'].strip()
            flow_capacity = float(
                row['Flow Capacity']) if row['Flow Capacity'] else 0
            distance = float(row['Distance Between Nodes']
                             ) if row['Distance Between Nodes'] else 0
            G.add_edge(source, destination,
                       flow_capacity=flow_capacity, distance=distance)

    return G


def style_water_network_graph():
    """
    Genera un gráfico estilizado del grafo como red de agua potable.
    """
    pos = nx.spring_layout(G, seed=42)  # Posiciones de los nodos

    # Aristas
    edge_x = []
    edge_y = []
    edge_text = []

    for edge in G.edges(data=True):
        src, dst, data = edge
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

        # Información sobre la arista (capacidad y distancia)
        edge_text.append(
            f"De {src} a {dst}<br>Capacidad: {data['flow_capacity']} L/s<br>Distancia: {data['distance']} km")

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=2, color='#0066cc'),
        hoverinfo='text',
        text=edge_text,
        mode='lines'
    )

    # Nodos
    node_x = []
    node_y = []
    node_text = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        # Información sobre el nodo
        connected_edges = list(G.edges(node, data=True))
        if connected_edges:
            capacities = [edge[2]['flow_capacity'] for edge in connected_edges]
            max_capacity = max(capacities)
            node_text.append(
                f"Estación: {node}<br>Capacidad máxima: {max_capacity} L/s")
        else:
            node_text.append(f"Estación: {node}<br>Sin conexiones")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=node_text,
        hoverinfo='text',
        marker=dict(
            size=20,
            color='#00cc99',
            line_width=2
        ),
        textposition="top center"
    )

    # Crear figura
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Red de Agua Potable",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=40),
        plot_bgcolor='white'
    )
    return fig


# Código principal para pruebas
if __name__ == "__main__":
    load_graph_from_csv('nodos_conectividad_3.csv')
    print(
        f"El grafo tiene {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas.")
    fig = style_water_network_graph()
    fig.show()
