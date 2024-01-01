import csv

def refinementCSV(archivo_entrada, archivo_salida):
    delimitador = ';'

    def procesar_valor(valor, limite, redondeo):
        while valor - limite > 0:
            valor /= 10
            valor = round(valor, redondeo)
        return str(valor)

    try:
        with open(archivo_entrada, 'r', newline='') as entrada, \
                open(archivo_salida, 'w', newline='') as salida:

            lector_csv = csv.reader(entrada, delimiter=delimitador)
            escritor_csv = csv.writer(salida, delimiter=delimitador)
            contador = 0

            filas = list(lector_csv)  # Leer todas las filas en memoria

            # Ordenar las filas por MMSI y tiempo (date y timestamp)
            filas.sort(key=lambda x: (x[4], x[2], x[3]))

            for fila in filas:
                if fila:
                    contador += 1

                    fila[0] = procesar_valor(float(fila[0]), 10, 5)
                    fila[1] = procesar_valor(float(fila[1]), 100, 4)

                    escritor_csv.writerow(fila)

                    print(f'Iteración {contador}: Valor primera columna: {fila[0]}')
                    print(f'Iteración {contador}: Valor segunda columna: {fila[1]}')

    except FileNotFoundError:
        print(f'Archivo "{archivo_entrada}" no encontrado.')
    except Exception as e:
        print(f'Ocurrió un error: {str(e)}')

    nuevas_filas = []

    with open(archivo_salida, 'r', newline='') as entrada:
        lector_csv = csv.reader(entrada, delimiter=';')

        for fila in lector_csv:
            if len(fila) >= 3:
                columnas = fila[2].split('T')
                if len(columnas) >= 2:
                    fila[2] = columnas[0]
                    fila.insert(6, columnas[1])

            nuevas_filas.append(fila)

    with open(archivo_salida, 'w', newline='') as salida:
        escritor_csv = csv.writer(salida, delimiter=';')

        for fila in nuevas_filas:
            escritor_csv.writerow(fila)

    print("Proceso completado. La columna 5 se ha agregado como columna 7 y se ha eliminado el contenido a partir del carácter 'T' en la tercera columna en el archivo de entrada con el delimitador ';' establecido.")
