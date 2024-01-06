import json
import random
from pymongo import MongoClient

def insertDB(archivo_geojson, nombre_coleccion, direccion_mongodb='localhost', puerto_mongodb=27017, nombre_base_datos='AISNorway'):
    # Configuración de conexión a MongoDB
    cliente = MongoClient(direccion_mongodb, puerto_mongodb)
    db = cliente[nombre_base_datos]
    coleccion = db[nombre_coleccion]

    # Carga el archivo GeoJSON como diccionario
    with open(archivo_geojson, 'r', encoding='utf-8') as geojson_file:
        geojson_data = json.load(geojson_file)

    # Inserta los datos en la colección de MongoDB
    coleccion.insert_many(geojson_data['features'])

    print(f"Los datos se han insertado en la colección '{nombre_coleccion}' de la base de datos '{nombre_base_datos}'.")



def obtener_mmsi_aleatorio(database_name, collection_name):
    # Conéctate a la base de datos MongoDB
    client = MongoClient('localhost', 27017)  # Ajusta la conexión según tu configuración
    db = client[database_name]
    collection = db[collection_name]

    # Obtén todos los MMSI únicos en la colección
    unique_mmsi = collection.distinct("properties.MMSI")

    # Selecciona aleatoriamente un MMSI de la lista
    mmsi_aleatorio = random.choice(unique_mmsi)

    # Cierra la conexión
    client.close()

    return mmsi_aleatorio

def information_random_MMSI(database_name, collection_name, mmsi, output_file):
    # Conéctate a la base de datos MongoDB
    client = MongoClient('localhost', 27017)
    db = client[database_name]
    collection = db[collection_name]

    # Realiza la consulta para obtener información por MMSI
    resultado = collection.find({'properties.MMSI': mmsi})

    # Lista para almacenar las entidades GeoJSON
    features = []

    # Itera sobre los documentos y agrega a la lista
    for document in resultado:
        feature = {
            "type": "Feature",
            "geometry": document['geometry'],
            "properties": document['properties']
        }
        features.append(feature)

    # Crear el objeto GeoJSON FeatureCollection
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    # Guardar el GeoJSON en un archivo
    with open(output_file, 'w') as f:
        json.dump(geojson_data, f, indent=2)

    # Cierra la conexión
    client.close()

