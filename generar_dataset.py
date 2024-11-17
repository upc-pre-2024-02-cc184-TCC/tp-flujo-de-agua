import pandas as pd
import random

# Definir nodos de las tablas proporcionadas
fuentes = [
    {"Fuente_ID": 1, "Nombre": "Río Rímac",
        "Ubicación": "Lima Centro", "Capacidad": 800000},
    {"Fuente_ID": 2, "Nombre": "Río Chillón",
        "Ubicación": "Lima Norte", "Capacidad": 500000},
    {"Fuente_ID": 3, "Nombre": "Río Lurín",
        "Ubicación": "Lima Sur", "Capacidad": 300000}
]

plantas = [
    {"Planta_ID": 1, "Nombre": "PTAP La Atarjea",
        "Ubicación": "Lima Centro", "Capacidad": 1200000},
    {"Planta_ID": 2, "Nombre": "PTAP Huachipa",
        "Ubicación": "Lima Este", "Capacidad": 1000000},
    {"Planta_ID": 3, "Nombre": "PTAP Chillón",
        "Ubicación": "Lima Norte", "Capacidad": 600000},
    {"Planta_ID": 4, "Nombre": "PTAP Surco",
        "Ubicación": "Lima Este", "Capacidad": 300000},
    {"Planta_ID": 5, "Nombre": "PTAP Pachacámac",
        "Ubicación": "Lima Sur", "Capacidad": 200000},
    {"Planta_ID": 6, "Nombre": "PTAP Villa El Salvador",
        "Ubicación": "Lima Sur", "Capacidad": 150000},
    {"Planta_ID": 7, "Nombre": "PTAP San Bartolo",
        "Ubicación": "Lima Sur", "Capacidad": 100000},
    {"Planta_ID": 8, "Nombre": "PTAP Santa Eulalia",
        "Ubicación": "Lima Este", "Capacidad": 80000},
    {"Planta_ID": 9, "Nombre": "PTAP Puente Piedra",
        "Ubicación": "Lima Norte", "Capacidad": 90000}
]

reservorios = [
    {"Reservorio_ID": 1, "Nombre": "Reservorio de La Atarjea",
        "Ubicación": "Lima Centro", "Capacidad": 500000},
    {"Reservorio_ID": 2, "Nombre": "Reservorio Puente Piedra",
        "Ubicación": "Lima Norte", "Capacidad": 300000},
    {"Reservorio_ID": 3, "Nombre": "Reservorio Villa El Salvador",
        "Ubicación": "Lima Sur", "Capacidad": 200000},
    {"Reservorio_ID": 4, "Nombre": "Reservorio de Huachipa",
        "Ubicación": "Lima Este", "Capacidad": 400000},
    {"Reservorio_ID": 5, "Nombre": "Reservorios en Ventanilla",
        "Ubicación": "Ventanilla", "Capacidad": 50000}
]

estaciones = [
    {"Estacion_ID": 1, "Nombre": "Estación de Bombeo de Atarjea",
        "Ubicación": "Lima Centro", "Capacidad": 3500},
    {"Estacion_ID": 2, "Nombre": "Estación de Bombeo de Huachipa",
        "Ubicación": "Lima Este", "Capacidad": 2000},
    {"Estacion_ID": 3, "Nombre": "Estación de Bombeo de Puente Piedra",
        "Ubicación": "Lima Norte", "Capacidad": 1500},
    {"Estacion_ID": 4, "Nombre": "Estaciones en Ventanilla",
        "Ubicación": "Ventanilla", "Capacidad": 800},
    {"Estacion_ID": 5, "Nombre": "Estación de Bombeo de Villa María",
        "Ubicación": "Lima Sur", "Capacidad": 1200}
]

# Mapear distritos a zonas
zonas = {
    "Lima Centro": ["Miraflores", "San Isidro", "Barranco", "Pueblo Libre", "San Miguel", "Magdalena del Mar", "Jesús María", "Lince", "Breña", "La Victoria", "Cercado de Lima", "Rímac"],
    "Lima Este": ["San Juan de Lurigancho", "La Molina", "Ate", "Santa Anita", "Cieneguilla", "El Agustino", "San Luis", "San Borja", "Santiago de Surco"],
    "Lima Norte": ["Comas", "Los Olivos", "Carabayllo", "Independencia", "San Martín de Porres", "Puente Piedra"],
    "Lima Sur": ["Villa El Salvador", "Villa María del Triunfo", "Pachacámac", "Pucusana", "San Bartolo", "Santa María del Mar", "Chilca", "Lurín", "Punta Hermosa", "Punta Negra", "San Juan de Miraflores"],
    "Ventanilla": ["Ventanilla"]
}

# Generar hogares adicionales
hogares = [
    {
        "Hogar_ID": i + (distritos.index(distrito) * 40),
        "Nombre": f"Hogar {distrito} {i}",
        "Ubicación": f"{zona}, {distrito}",
        "Capacidad": random.randint(20000, 60000)
    }
    for zona, distritos in zonas.items()
    for distrito in distritos
    for i in range(1, 41)
]

# Crear conexiones siguiendo el flujo lógico: Ríos -> Plantas -> Reservorios -> Estaciones -> Hogares
connections = []

# Ríos a plantas
for fuente in fuentes:
    for planta in plantas:
        if fuente["Nombre"] == "Río Rímac":
            if planta["Ubicación"] == "Lima Norte":
                distance = random.randint(1500, 4000)
            elif planta["Ubicación"] == "Lima Centro":
                distance = random.randint(500, 2000)
            elif planta["Ubicación"] == "Lima Este":
                distance = random.randint(2000, 5000)
            else:
                continue 
        elif fuente["Nombre"] == "Río Chillón":
            if planta["Ubicación"] == "Lima Norte":
                distance = random.randint(500, 2000)
            elif planta["Ubicación"] == "Lima Centro":
                distance = random.randint(1800, 4500)
            else:
                continue 
        elif fuente["Nombre"] == "Río Lurín":
            if planta["Ubicación"] == "Lima Sur":
                distance = random.randint(500, 3000)
            elif planta["Ubicación"] == "Lima Este":
                distance = random.randint(2500, 6000)
            else:
                continue
        else:
            continue 

        connections.append({
            "Source Node": fuente["Nombre"],
            "Destination Node": planta["Nombre"],
            "Node Type": "Water Treatment Plant",
            "Flow Capacity": min(fuente["Capacidad"], planta["Capacidad"]),
            "Distance Between Nodes": distance
        })


# Plantas a reservorios
for planta in plantas:
    for reservorio in reservorios:
        if (reservorio["Ubicación"] == planta["Ubicación"]) or (
            planta["Nombre"] == "PTAP Puente Piedra" and reservorio["Ubicación"] == "Ventanilla"
        ):
            connections.append({
                "Source Node": planta["Nombre"],
                "Destination Node": reservorio["Nombre"],
                "Node Type": "Storage Tank",
                "Flow Capacity": min(planta["Capacidad"], reservorio["Capacidad"]),
                "Distance Between Nodes": random.randint(1500, 2000)
            })


# Reservorios a estaciones
for reservorio in reservorios:
    for estacion in estaciones:
        if estacion["Ubicación"] == reservorio["Ubicación"]:
            connections.append({
                "Source Node": reservorio["Nombre"],
                "Destination Node": estacion["Nombre"],
                "Node Type": "Pumping Station",
                "Flow Capacity": min(reservorio["Capacidad"], estacion["Capacidad"]),
                "Distance Between Nodes": random.randint(200, 800)
            })

# Estaciones a hogares
for estacion in estaciones:
    for hogar in hogares:
        if hogar["Ubicación"].startswith(estacion["Ubicación"].split(",")[0]):
            connections.append({
                "Source Node": estacion["Nombre"],
                "Destination Node": hogar["Nombre"],
                "Node Type": "Consumption Point",
                "Flow Capacity": hogar["Capacidad"],
                "Distance Between Nodes": random.randint(100, 500)
            })

# Crear DataFrame
df_connections = pd.DataFrame(connections)

# Guardar en archivo CSV
output_path = "nodos_conectividad_3.csv"
df_connections.to_csv(output_path, index=False)
output_path
