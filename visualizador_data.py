'''
    Crea templates para archivos de lenguajes de
    programacion.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-


# Librerias estandar.
import sys
import csv

from calificacion_codigo import cal_codi



# Guarda los datos generados en un arhcivo permanente.
def open_data(direccion_archivo):

    with open(direccion_archivo, newline='') as objeto_archivo:
        reader = csv.DictReader(objeto_archivo)
        columnas = reader.fieldnames

        datos = {}
        for columna in columnas:
            datos[columna] = []

        for fila in reader:
            for columna in columnas:
                datos[columna].append(fila[columna])

    return datos


# Califica los reportes del 1 al 9 dependiendo de la severidad.
def calificar(reportes, codigos):
    nuevos_datos = {}
    for codigo in codigos:
        cal_base = cal_codi[codigo][0]
        cal_reportes = cal_codi[codigo][1]

        nuevos_datos[codigo] = {
            'ocurrencias': reportes[codigo][0],
            'cal_base': cal_base,
            'reportes': {}
        }

        for reporte in reportes[codigo][1]:
            if reporte in list(cal_codi[codigo][1].keys()):
                cal_reporte = cal_codi[codigo][1][reporte]
            else:
                cal_reporte = 0
            nuevos_datos[codigo]['reportes'][reporte] = cal_base + cal_reporte

    return nuevos_datos


def procesar_datos(datos):
    codigos = []
    ocurrencias = {}
    for desc, cod in zip(datos['crimedescr'], datos['ucr_ncic_code']):
        cod = int(cod)
        if cod not in codigos:
            codigos.append(cod)
            ocurrencias[cod] = [1, [desc]]
        else:
            ocurrencias[cod][0] += 1
            if desc not in ocurrencias[cod][1]:
                ocurrencias[cod][1].append(desc)

    codigos = sorted(codigos)
    return codigos, ocurrencias


def formatear_datos(ocurrencias, codigos):
    datos_procesados = "Total de codigos: {}\n\n".format(len(codigos))
    for codigo in codigos:
        datos = ocurrencias[codigo]
        reportes = datos['reportes']
        datos_procesados += 'Codigo: {}\nCantidad de ocurrencias: {}\nReportes:\n'.format(codigo, datos['ocurrencias'])
        for reporte in reportes:
            datos_procesados += '\t{}\tcalificación: {}\n'.format(reporte, reportes[reporte])
        datos_procesados += '\n' + '-'*20 + '\n'

    return datos_procesados


# Funcion main.
def main(args):
    datos = open_data(args[0])

    codigos, ocurrencias = procesar_datos(datos)

    reportes_calificados = calificar(ocurrencias, codigos)

    datos_formateados = formatear_datos(reportes_calificados, codigos)
    print(datos_formateados)

    # Guardamos la ponderacion por codigo y reporte.
    objeto_archivo = open('datos_procesados.txt', 'w')
    objeto_archivo.write(datos_formateados)
    objeto_archivo.close()



if __name__ == "__main__":
    main(sys.argv[1:])
