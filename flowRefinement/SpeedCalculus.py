import geojson
import json
import math

def HaversineFunction(lat1, lon1, lat2, lon2):

    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Fórmula Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radio de la Tierra en kilómetros

    # Calcular la distancia en metros
    distancia = r * c * 1000  # Convertir de kilómetros a metros
    return distancia

def speedCalculus(file_path):
    # Abre y lee el archivo GeoJSON
    with open(file_path, 'r') as geojson_file:
        data = geojson.load(geojson_file)

    # Obtén la lista de features (elementos)
    features = data['features']

    # Realiza la resta de timestamp_sec y cálculo de distancia para elementos consecutivos
    for i in range(1, len(features)):
        elemento_anterior = features[i - 1]['properties']['timestamp_sec']
        elemento_actual = features[i]['properties']['timestamp_sec']

        # Obtén las coordenadas geográficas de los elementos
        coords_anterior = features[i - 1]['geometry']['coordinates']
        coords_actual = features[i]['geometry']['coordinates']

        # Calcula la distancia utilizando la función Haversine
        distancia = HaversineFunction(coords_anterior[0], coords_anterior[1], coords_actual[0], coords_actual[1])
        tiempo = elemento_actual - elemento_anterior

        # Inicializa la velocidad, distancia y tiempo como 0
        velocidad_kmph = 0
        velocidad_nudos = 0

        # Calcula la velocidad, distancia y tiempo si el tiempo es mayor que 0
        if tiempo > 0:
            # Calcula la velocidad en metros por segundo (m/s)
            velocidad_ms = distancia / tiempo

            # Convierte la velocidad a kilómetros por hora (km/h) y nudos (kt)
            velocidad_kmph = round(velocidad_ms * 3.6, 4)
            velocidad_nudos = round(velocidad_ms * 1.94384, 4)

        # Añade las velocidades, distancia, tiempo_gap como nuevas propiedades en las propiedades de la feature
        features[i]['properties']['distance'] = distancia
        features[i]['properties']['time_gap'] = tiempo
        features[i]['properties']['speed_kmh'] = velocidad_kmph
        features[i]['properties']['speed_knot'] = velocidad_nudos


        print(f"Velocidad entre elemento {i} y elemento {i - 1}:")
        print(f" - {velocidad_kmph} km/h")
        print(f" - {velocidad_nudos} nudos")
        print(f"Distancia entre elemento {i} y elemento {i - 1}: {distancia} metros")
        print(f"Tiempo gap entre elemento {i} y elemento {i - 1}: {tiempo} segundos")

    # Añade manualmente el valor 0 para el primer elemento
    features[0]['properties']['distance'] = 0
    features[0]['properties']['time_gap'] = 0
    features[0]['properties']['speed_kmh'] = 0
    features[0]['properties']['speed_knot'] = 0


    # Guarda el archivo GeoJSON con las nuevas propiedades
    with open(file_path, 'w') as geojson_file:
        geojson.dump(data, geojson_file, indent=2)

    print(f"Archivo '{file_path}' actualizado con éxito.")


def modifyTimestamp(ruta_archivo_geojson_original, ruta_archivo_geojson_nuevo):
    # Función para convertir una marca de tiempo a segundos
    def timestamp_to_seconds(timestamp):
        partes_timestamp = timestamp.split(':')
        if len(partes_timestamp) == 3:
            horas, minutos, resto = partes_timestamp
            segundos, milisegundos_z = resto.split('.')
            milisegundos = milisegundos_z[:-1]
            total_segundos = int(horas) * 3600 + int(minutos) * 60 + int(segundos) + int(milisegundos) / 1000
            return total_segundos
        return None

    # Abre el archivo original y carga su contenido como un objeto JSON
    with open(ruta_archivo_geojson_original, 'r') as archivo_original:
        geojson_data = json.load(archivo_original)

    # Itera a través de las características y agrega la nueva propiedad "timestamp_sec"
    for feature in geojson_data['features']:
        properties = feature['properties']
        if 'timestamp' in properties:
            timestamp = properties['timestamp']
            total_segundos = timestamp_to_seconds(timestamp)
            if total_segundos is not None:
                properties['timestamp_sec'] = total_segundos

    # Guarda el archivo GeoJSON con la nueva propiedad "timestamp_sec"
    with open(ruta_archivo_geojson_nuevo, 'w') as archivo_nuevo:
        json.dump(geojson_data, archivo_nuevo, indent=2)

    print(f"Archivo '{ruta_archivo_geojson_nuevo}' generado con éxito.")

