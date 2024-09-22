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
    flow_capacity = float(row['Flow Capacity (L/s)']) if pd.notnull(row['Flow Capacity (L/s)']) else 0
    distance = float(row['Distance Between Nodes (km)']) if pd.notnull(row['Distance Between Nodes (km)']) else 0
    G.add_edge(source, destination, flow_capacity=flow_capacity, distance=distance)

# Lista de nodos
nodes = list(G.nodes())

# Crear la app de Dash
app = dash.Dash(__name__)

# Diseño de la página web
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'backgroundColor': '#f4f4f4', 'padding': '20px'}, children=[
    html.H1("Visualización de Red de Flujos de Agua", style={'text-align': 'center', 'color': '#2c3e50'}),

    # Menú desplegable para seleccionar nodo
    html.Div([
        html.Label("Selecciona un Nodo", style={'font-size': '18px', 'margin-right': '10px'}),
        dcc.Dropdown(
            id='node-selector',
            options=[{'label': node, 'value': node} for node in nodes],
            value=nodes[0],
            clearable=False,
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),

    # Mostrar gráfico interactivo
    dcc.Graph(id='network-graph'),

    # Mostrar los flujos en texto
    html.Div(id='flow-info', style={'margin-top': '20px', 'padding': '10px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px'})
])


# Función para crear la visualización del grafo
def create_graph(selected_node):
    # Obtener posiciones de los nodos
    pos = nx.spring_layout(G, seed=42)

    # Listas para los elementos gráficos
    edge_x = []
    edge_y = []
    edge_text = []
    node_x = []
    node_y = []
    node_text = []
    node_color = []

    # Obtener los nodos y aristas conectadas al nodo seleccionado
    incoming_edges = G.in_edges(selected_node, data=True)
    outgoing_edges = G.out_edges(selected_node, data=True)

    # Dibujar nodos y aristas para los flujos entrantes y salientes
    connected_nodes = set([selected_node])
    connected_edges = list(incoming_edges) + list(outgoing_edges)

    for edge in connected_edges:
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
        connected_nodes.add(src)
        connected_nodes.add(dst)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#7f8c8d'),
        hoverinfo='text',
        text=edge_text,
        mode='lines'
    )

    # Agregar los nodos conectados
    for node in connected_nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(f"Estación: {node}")
        # Colorear el nodo seleccionado en rojo, el resto en azul
        if node == selected_node:
            node_color.append('red')
        else:
            node_color.append('blue')

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hoverinfo='text',
        marker=dict(
            size=20,
            color=node_color,
            line_width=2
        ),
        textposition="top center"
    )

    fig = go.Figure(data=[edge_trace, node_trace])

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
     Output('flow-info', 'children')],
    [Input('node-selector', 'value')]
)
def update_graph(selected_node):
    # Crear gráfico interactivo del grafo con nodos conectados
    graph_figure = create_graph(selected_node)

    # Obtener los flujos entrantes y salientes para el nodo seleccionado
    incoming_edges = G.in_edges(selected_node, data=True)
    outgoing_edges = G.out_edges(selected_node, data=True)

    incoming_info = html.Div([
        html.H4("Flujos Entrantes", style={'color': '#2980b9'}),
        html.Ul([html.Li(f"Desde {src} - Capacidad: {data['flow_capacity']} L/s") for src, _, data in incoming_edges])
    ])

    outgoing_info = html.Div([
        html.H4("Flujos Salientes", style={'color': '#27ae60'}),
        html.Ul([html.Li(f"Hacia {dst} - Capacidad: {data['flow_capacity']} L/s") for _, dst, data in outgoing_edges])
    ])

    return graph_figure, [incoming_info, outgoing_info]


if __name__ == '__main__':
    app.run_server(debug=True)
