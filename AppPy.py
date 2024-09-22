import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import networkx as nx
import pandas as pd
import plotly.graph_objects as go

# Crear el grafo
G = nx.DiGraph()

# Leer el archivo CSV
df = pd.read_csv('nodos_conectividad.csv')
for index, row in df.iterrows():
    source = row['Source Node'].strip()
    destination = row['Destination Node'].strip()
    flow_capacity = float(row['Flow Capacity']
                          ) if pd.notnull(row['Flow Capacity']) else 0
    distance = float(row['Distance Between Nodes']) if pd.notnull(
        row['Distance Between Nodes']) else 0
    G.add_edge(source, destination,
               flow_capacity=flow_capacity, distance=distance)

# Lista de nodos
nodes = list(G.nodes())

# Crear la app de Dash
app = dash.Dash(__name__)

# Diseño de la página web
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'backgroundColor': '#f4f4f4', 'padding': '20px'}, children=[
    html.H1("Optimización y Visualización de Red de Agua",
            style={'text-align': 'center', 'color': '#2c3e50'}),

    # Menú desplegable para seleccionar algoritmo
    html.Div([
        html.Label("Selecciona Algoritmo", style={
                   'font-size': '18px', 'margin-right': '10px'}),
        dcc.Dropdown(
            id='algorithm-selector',
            options=[
                {'label': 'Seleccionar', 'value': 'none'},
                {'label': 'Ruta Óptima - Bellman-Ford', 'value': 'bellman-ford'}
            ],
            value='none',
            clearable=False,
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),

    # Menú desplegable para seleccionar nodo origen
    html.Div([
        html.Label("Selecciona Nodo Origen", style={
                   'font-size': '18px', 'margin-right': '10px'}),
        dcc.Dropdown(
            id='node-selector-origin',
            options=[{'label': 'Seleccionar', 'value': 'none'}] + \
            [{'label': node, 'value': node} for node in nodes],
            value='none',
            clearable=False,
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),

    # Menú desplegable para seleccionar nodo destino
    html.Div([
        html.Label("Selecciona Nodo Destino", style={
                   'font-size': '18px', 'margin-right': '10px'}),
        dcc.Dropdown(
            id='node-selector-destination',
            options=[{'label': 'Seleccionar', 'value': 'none'}] + \
            [{'label': node, 'value': node} for node in nodes],
            value='none',
            clearable=False,
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),

    # Mostrar gráfico interactivo
    dcc.Graph(id='network-graph'),

    # Mostrar información de optimización
    html.Div(id='optimization-info', style={'margin-top': '20px',
             'padding': '10px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px'})
])

# Función de Bellman-Ford para rutas óptimas


def apply_bellman_ford(source, target):
    try:
        length, path = nx.single_source_bellman_ford(
            G, source, weight='distance')
        return length[target], path[target]
    except nx.NetworkXNoPath:
        return float('inf'), []

# Función para crear la visualización del grafo


def create_graph(selected_node, path_edges=None):
    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    edge_text = []
    node_x = []
    node_y = []
    node_text = []
    node_color = []

    # Dibujar nodos y aristas del grafo original
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
        flow_capacity = data['flow_capacity']
        edge_text.append(f"De {src} a {dst} - Capacidad: {flow_capacity} L/s")

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#7f8c8d'),
        hoverinfo='text',
        text=edge_text,
        mode='lines'
    )

    # Dibujar la ruta seleccionada en rojo
    if path_edges:
        path_edge_x = []
        path_edge_y = []
        for src, dst in path_edges:
            x0, y0 = pos[src]
            x1, y1 = pos[dst]
            path_edge_x.append(x0)
            path_edge_x.append(x1)
            path_edge_x.append(None)
            path_edge_y.append(y0)
            path_edge_y.append(y1)
            path_edge_y.append(None)

        path_trace = go.Scatter(
            x=path_edge_x, y=path_edge_y,
            line=dict(width=3, color='red'),
            mode='lines'
        )
    else:
        path_trace = go.Scatter()

    # Agregar nodos al grafo
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"Estación: {node}")
        node_color.append('blue' if node != selected_node else 'red')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hoverinfo='text',
        marker=dict(size=20, color=node_color, line_width=2),
        textposition="top center"
    )

    fig = go.Figure(data=[edge_trace, path_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white'
    )
    return fig


@app.callback(
    [Output('network-graph', 'figure'),
     Output('optimization-info', 'children')],
    [Input('algorithm-selector', 'value'),
     Input('node-selector-origin', 'value'),
     Input('node-selector-destination', 'value')]
)
def update_graph_and_optimization(selected_algorithm, selected_origin, selected_destination):
    # Validar si los nodos de origen y destino son iguales
    if selected_origin == selected_destination:
        return create_graph(None), "No se puede seleccionar el mismo nodo como origen y destino."

    # Evitar la ejecución si no se seleccionan nodos
    if selected_origin == 'none' or selected_destination == 'none':
        return create_graph(None), "Selecciona nodos de origen y destino."

    # Si no existe un camino posible
    if not nx.has_path(G, selected_origin, selected_destination):
        possible_targets = [
            node for node in nodes if nx.has_path(G, selected_origin, node)]
        return create_graph(None), f"No hay caminos disponibles hacia {selected_destination}. Nodos posibles: {possible_targets}"

    # Crear el grafo inicial
    graph_figure = create_graph(selected_origin)

    if selected_algorithm == 'bellman-ford':
        length, path = apply_bellman_ford(
            selected_origin, selected_destination)
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        graph_figure = create_graph(selected_origin, path_edges)

        # Aquí verificamos el camino y sumamos la distancia real
        total_distance = sum(G[path[i]][path[i+1]]['distance']
                             for i in range(len(path) - 1))

        optimization_text = (f"Ruta óptima calculada con Bellman-Ford desde {selected_origin} a {selected_destination}: "
                             f"{path}. Distancia total: {total_distance} km.")
        return graph_figure, optimization_text

    return graph_figure, "Selecciona un algoritmo para calcular la ruta óptima."


if __name__ == '__main__':
    app.run_server(debug=True)
