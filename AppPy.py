import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from GrafoCSV import load_graph_from_csv, style_water_network_graph  # Importar funciones
from bellman_ford import apply_bellman_ford
from ford_fulkerson import apply_ford_fulkerson

# Cargar el grafo desde el archivo CSV
G = load_graph_from_csv('nodos_conectividad_3.csv')
nodes = list(G.nodes())

# Crear la app de Dash
app = dash.Dash(__name__)

# Diseño de la página web
app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'backgroundColor': '#eaf7ff', 'padding': '20px'},
                      children=[
                          html.H1("TCC Group LIMA - Red de Agua Potable",
                                  style={'text-align': 'center', 'color': '#0056b3', 'margin-bottom': '40px'}),

                          # Primera sección: Opciones iniciales
                          html.Div(
                              style={'display': 'flex', 'flexWrap': 'wrap', 'justify-content': 'space-between', 'margin-bottom': '40px'},
                              children=[
                                  html.Div(style={'width': '48%', 'backgroundColor': '#d7eaf8', 'padding': '20px',
                                                  'borderRadius': '10px'}, children=[
                                      html.H3("Seleccione nodos:", style={'color': '#0056b3'}),
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
                                  html.Div(style={'width': '48%', 'backgroundColor': '#d7eaf8', 'padding': '20px',
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
                                          'margin-bottom': '40px'}, children=[
                              html.H3("Resultado:", style={'color': '#0056b3', 'margin-bottom': '10px'}),
                              html.Div(id='optimization-info', style={'color': '#003366', 'fontSize': '16px'})
                          ]),

                          # Tercera sección: Gráfico interactivo
                          html.Div(style={'backgroundColor': '#f0f8ff', 'padding': '20px', 'borderRadius': '10px'},
                                   children=[
                                       dcc.Graph(
                                           id='network-graph',
                                           figure=style_water_network_graph(),  # Grafo estilizado
                                           style={'height': '600px'}  # Aumentar la altura del gráfico
                                       )
                                   ])
                      ])


# Callback para manejar la interacción con los algoritmos
@app.callback(
    Output('optimization-info', 'children'),
    Input('node-selector-origin', 'value'),
    Input('node-selector-destination', 'value'),
    Input('algorithm-selector', 'value')
)
def calculate_algorithm_result(origin, destination, algorithm):
    # Validar entradas
    if not origin or not destination or not algorithm:
        return "Seleccione un nodo de origen, un nodo de destino y un algoritmo."

    if origin == destination:
        return "El nodo de origen y destino no pueden ser iguales."

    if algorithm == 'bellman-ford':
        # Aplicar Bellman-Ford para ruta óptima
        distance, path = apply_bellman_ford(G, origin, destination)
        if distance == float('inf'):
            return f"No hay una ruta disponible entre {origin} y {destination}."
        else:
            path_str = " -> ".join(path)
            return f"Ruta óptima desde {origin} a {destination}: {path_str}<br>Distancia total: {distance} km"

    elif algorithm == 'ford-fulkerson':
        # Aplicar Ford-Fulkerson para flujo máximo
        flow_value, flow_dict = apply_ford_fulkerson(G, origin, destination)
        return f"Flujo máximo desde {origin} a {destination}: {flow_value} L/s."

    return "Error: Algoritmo no reconocido."


if __name__ == '__main__':
    app.run_server(debug=True)
