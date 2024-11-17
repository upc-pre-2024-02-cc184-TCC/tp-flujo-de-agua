import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
from bellman_ford import apply_bellman_ford
from ford_fulkerson import apply_ford_fulkerson

# Crear el grafo
G = nx.DiGraph()

# Leer el archivo CSV
df = pd.read_csv('Grafo.csv')
for index, row in df.iterrows():
    source = row['Source Node'].strip()
    destination = row['Destination Node'].strip()
    flow_capacity = float(row['Flow Capacity']) if pd.notnull(row['Flow Capacity']) else 0
    distance = float(row['Distance Between Nodes']) if pd.notnull(row['Distance Between Nodes']) else 0
    G.add_edge(source, destination, flow_capacity=flow_capacity, distance=distance)

# Lista de nodos
nodes = list(G.nodes())

# Crear la app de Dash
app = dash.Dash(__name__)

# Diseño de la página web
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'backgroundColor': '#eaf7ff', 'padding': '20px'},
                      children=[
                          html.H1("TCC Group LIMA",
                                  style={'text-align': 'center', 'color': '#0056b3', 'margin-bottom': '40px'}),

                          # Primera sección: Opciones iniciales
                          html.Div(
                              style={'display': 'flex', 'justify-content': 'space-around', 'margin-bottom': '30px'},
                              children=[
                                  html.Div(style={'width': '30%', 'backgroundColor': '#d7eaf8', 'padding': '15px',
                                                  'borderRadius': '10px'}, children=[
                                      html.H3("Seleccione una de las opciones:", style={'color': '#0056b3'}),
                                      dcc.Dropdown(
                                          id='node-selector-origin',
                                          options=[{'label': node, 'value': node} for node in nodes],
                                          placeholder='Selecciona nodo de origen',
                                          style={'margin-bottom': '20px'}
                                      ),
                                      dcc.Dropdown(
                                          id='node-selector-destination',
                                          options=[{'label': node, 'value': node} for node in nodes],
                                          placeholder='Selecciona nodo de destino',
                                          style={'margin-bottom': '20px'}
                                      )
                                  ]),
                                  html.Div(style={'width': '30%', 'backgroundColor': '#d7eaf8', 'padding': '15px',
                                                  'borderRadius': '10px'}, children=[
                                      html.H3("Seleccione algoritmo:", style={'color': '#0056b3'}),
                                      dcc.Dropdown(
                                          id='algorithm-selector',
                                          options=[
                                              {'label': 'Ruta Óptima - Bellman-Ford', 'value': 'bellman-ford'},
                                              {'label': 'Flujo Máximo - Ford-Fulkerson', 'value': 'ford-fulkerson'}
                                          ],
                                          placeholder='Selecciona un algoritmo',
                                          style={'margin-bottom': '20px'}
                                      )
                                  ])
                              ]),

                          # Segunda sección: Resultado
                          html.Div(style={'backgroundColor': '#cce5ff', 'padding': '20px', 'borderRadius': '10px',
                                          'margin-bottom': '30px'}, children=[
                              html.H3("Resultado:", style={'color': '#0056b3', 'margin-bottom': '10px'}),
                              html.Div(id='optimization-info', style={'color': '#003366', 'fontSize': '16px'})
                          ]),

                          # Tercera sección: Gráfico interactivo
                          html.Div(style={'backgroundColor': '#f0f8ff', 'padding': '20px', 'borderRadius': '10px'},
                                   children=[
                                       dcc.Graph(id='network-graph')
                                   ])
                      ])

def create_graph(selected_node, path_edges=None, flow_dict=None):
    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    edge_text = []
    node_x = []
    node_y = []
    node_text = []
    node_color = []

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
        edge_text.append(f"De {src} a {dst} - Capacidad: {data['flow_capacity']} L/s")

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#7f8c8d'),
        hoverinfo='text',
        text=edge_text,
        mode='lines'
    )

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

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        margin=dict(b=0, l=0, r=0, t=0),
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
    if selected_origin == selected_destination:
        return create_graph(None), "No se puede seleccionar el mismo nodo como origen y destino."

    if not selected_algorithm or not selected_origin or not selected_destination:
        return create_graph(None), "Selecciona todos los campos necesarios."

    if selected_algorithm == 'bellman-ford':
        length, path = apply_bellman_ford(G, selected_origin, selected_destination)
        return create_graph(selected_origin), f"Distancia óptima: {length} km. Ruta: {path}"

    elif selected_algorithm == 'ford-fulkerson':
        flow_value, _ = apply_ford_fulkerson(G, selected_origin, selected_destination)
        return create_graph(selected_origin), f"Flujo máximo: {flow_value} L/s."

    return create_graph(None), "Selecciona un algoritmo."

if __name__ == '__main__':
    app.run_server(debug=True)