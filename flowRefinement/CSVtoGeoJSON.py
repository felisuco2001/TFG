import csv
import geojson


def csvToGeoJSON(archivo_csv, archivo_geojson):
    # Abre el archivo CSV en modo lectura
    with open(archivo_csv, 'r', newline='', encoding='utf-8') as csv_file:
        lector_csv = csv.reader(csv_file, delimiter=';')

        # Lee la primera fila del archivo CSV como encabezados
        encabezados = next(lector_csv)

        # Inicializa una lista para almacenar las Features GeoJSON
        features = []

        # Itera sobre cada fila del archivo CSV
        for fila in lector_csv:
            # Crea una Feature GeoJSON para cada par de coordenadas con su correspondiente timestamp y date
            geometry = geojson.Point([float(fila[1]), float(fila[0])])  # Latitud y longitud

            properties = {
                "date": fila[2],
                "name": fila[3],
                "MMSI": fila[4],
                "IMO": fila[5],
                "timestamp": fila[6],
                "callsign": fila[7]
            }

            feature = geojson.Feature(geometry=geometry, properties=properties)
            features.append(feature)

    # Crea un objeto FeatureCollection GeoJSON con todas las características
    feature_collection = geojson.FeatureCollection(features)

    # Escribe el objeto GeoJSON en el archivo de salida con saltos de línea
    with open(archivo_geojson, 'w', encoding='utf-8') as geojson_file:
        geojson.dump(feature_collection, geojson_file, ensure_ascii=False, indent=2)


    print(f"Transformación completa. Se ha creado el archivo GeoJSON: {archivo_geojson}")


