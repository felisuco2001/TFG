import json
import csv

def geojson_to_csv(geojson_path, csv_path):
    # Cargar el contenido del archivo GeoJSON
    with open(geojson_path, 'r') as geojson_file:
        geojson_data = json.load(geojson_file)

    # Abrir el archivo CSV para escribir
    with open(csv_path, 'w', newline='') as csv_file:
        # Crear un objeto escritor CSV con punto y coma como delimitador
        csv_writer = csv.writer(csv_file, delimiter=';')

        # Iterar sobre las características en el archivo GeoJSON
        for feature in geojson_data['features']:
            # Obtener las coordenadas y propiedades
            coordinates = feature['geometry']['coordinates']
            timestamp = feature['properties']['timestamp']
            date = feature['properties']['date']

            # Cambiar el punto por coma en las coordenadas
            coordinates[0] = str(coordinates[0]).replace('.', ',')
            coordinates[1] = str(coordinates[1]).replace('.', ',')

            # Escribir una fila en el archivo CSV
            csv_writer.writerow([coordinates[0], coordinates[1], timestamp, date])

    print(f"La conversión se ha completado. El archivo CSV se encuentra en: {csv_path}")

# Rutas de entrada y salida
geojson_path = r'C:\Users\felix\PycharmProjects\TFG\PruebaFlujoAISData\testRandomMMSI.geojson'
csv_path = r'C:\Users\felix\PycharmProjects\TFG\PruebaFlujoAISData\testRandomMMSI.csv'

# Llamar a la función
geojson_to_csv(geojson_path, csv_path)
