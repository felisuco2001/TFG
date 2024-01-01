from flowRefinement.SpeedCalculus import speedCalculus
from flowRefinement.CSVtoGeoJSON import csvToGeoJSON
from flowRefinement.SpeedCalculus import modifyTimestamp
from flowRefinement.RefinementCSV import refinementCSV
from flowRefinement.uploadBBDD import insertDB, obtener_mmsi_aleatorio,information_random_MMSI

archivo_entrada = r'C:\Users\Felix\Desktop\PruebaFlujoAISData\dataNorway.csv'
archivo_salida = r'C:\Users\Felix\Desktop\PruebaFlujoAISData\dataNorwayFixed.csv'
archivo_geojson = r'C:\Users\Felix\Desktop\PruebaFlujoAISData\dataNorway.geojson'
archivo_salida_geojson = r'C:\Users\Felix\Desktop\PruebaFlujoAISData\dataNorwayFixed.geojson'
test_geojson = r'C:\Users\Felix\Desktop\PruebaFlujoAISData\testRandomMMSI.geojson'
nombre_coleccion = 'Vessels_August'
nombre_coleccion_test = 'Tests_Statistics'
direccion_mongodb = 'localhost'
puerto_mongodb = 27017
nombre_base_datos = 'AIS'
nombre_base_datos_tests = 'AIS_Tests'

refinementCSV(archivo_entrada, archivo_salida)
csvToGeoJSON(archivo_salida, archivo_geojson)
modifyTimestamp(archivo_geojson, archivo_salida_geojson)
speedCalculus(archivo_salida_geojson)
insertDB(archivo_salida_geojson, nombre_coleccion, direccion_mongodb, puerto_mongodb, nombre_base_datos)
mmsi = obtener_mmsi_aleatorio("AIS", "Vessels_August")
information_random_MMSI("AIS", nombre_coleccion, mmsi, test_geojson)
insertDB(test_geojson, nombre_coleccion_test, direccion_mongodb, puerto_mongodb, nombre_base_datos_tests)
