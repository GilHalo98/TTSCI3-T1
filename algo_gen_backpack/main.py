'''
    Algoritmos genericos para resolver el problema de la mochila.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "Diego Gil"


# Librerias estandar.
import argparse
import csv
import pickle

# Librerias propias
from util.clases.poblacion import Poblacion


# Formatea los argumentos pasados por consola.
def format_args():
    args_parser = argparse.ArgumentParser(
        description='Problema de la mochila resuelto con algoritmos geneticos'
    )

    args_parser.add_argument(
        '--problema',
        default=None,
        help='Directorio o nombre del archivo problema, es un archivo csv',
        dest='dir_archivo',
        type=str,
    )

    args_parser.add_argument(
        '--pesoMax',
        default=None,
        help='Peso maximo cargado por la mochila',
        dest='peso_max',
        type=int,
    )

    args_parser.add_argument(
        '--generacionesMax',
        default=10,
        help='Maximo de generaciones que se pueden producir',
        dest='generaciones_max',
        type=int,
    )

    args_parser.add_argument(
        '--poblacionIni',
        default=10,
        help='Poblacion inicial del algoritmo',
        dest='poblacion_inicial',
        type=int,
    )

    args_parser.add_argument(
        '--poblacionMax',
        default=-1,
        help='Poblacion maxima que se puede alcanzar',
        dest='poblacion_max',
        type=int,
    )

    args_parser.add_argument(
        '--probMutacion',
        default=0.01,
        help='Probabilidad de mutacion del cromosoma',
        dest='probabilidad_mutacion',
        type=float
    )

    args_parser.add_argument(
        '--archivosSalida',
        default='resultado',
        help='Probabilidad de mutacion del cromosoma',
        dest='archivos_salida',
        type=str
    )

    args = args_parser.parse_args()

    return args


# Carga el problema del archivo csv.
def cargar_problema(dir_archivo, type_val):
    # Instancia donde se guarda el problema.
    problema = {}

    print('Abriendo archivo: {}'.format(dir_archivo))
    with open(dir_archivo, newline='') as archivo:
        objeto_archivo = csv.DictReader(archivo)

        propiedades = objeto_archivo.fieldnames

        for propiedad in propiedades:
            problema[propiedad] = []

        for fila in objeto_archivo:
            for propiedad in propiedades:
                problema[propiedad].append(type_val(fila[propiedad]))

    longitud = len(problema[propiedades[0]])

    return problema, longitud


# Guarda el resultado en un archivo de texto.
def guardar(nombre_archivo, datos, param_sol):
    # Abre o crea y abre el archivo y guarda los datos.
    with open(nombre_archivo, 'w+') as archivo:
        parametros_solucion = 'Parametros de solucion del problema {}:'
        parametros_solucion += '\n\t Peso Maximo {}'
        parametros_solucion += '\n\t Generaciones Maximas {}'
        parametros_solucion += '\n\t Poblacion Inicial {}'
        parametros_solucion += '\n\t Poblacion Maxima {}'
        parametros_solucion += '\n\t Probabilidad de mutacion {}'
        parametros_solucion += '\n\t Total de genes {}\n'

        archivo.write(parametros_solucion.format(*param_sol))
        archivo.write(datos)


# Guarda un archivo con el registro serializado.
def serializar(nombre_archivo, datos):
    # Abre o crea y abre el archivo y guarda los datos.
    with open(nombre_archivo, 'wb+') as archivo:
        pickle.dump(datos, archivo)


# Funcion main.
def main(con_args, *args, **kargs):
    dir_archivo = con_args.dir_archivo
    peso_max = con_args.peso_max
    generaciones_max = con_args.generaciones_max
    poblacion_inicial = con_args.poblacion_inicial
    poblacion_max = con_args.poblacion_max
    probabilidad_mutacion = con_args.probabilidad_mutacion
    archivos_salida = con_args.archivos_salida

    instancia, longitud = cargar_problema(dir_archivo, int)

    poblacion = Poblacion(
        poblacion_inicial,
        generaciones_max,
        poblacion_max,
        [longitud, instancia, peso_max, probabilidad_mutacion]
    )

    poblacion.run()

    parametros_solucion = [
        dir_archivo,
        peso_max,
        generaciones_max,
        poblacion_inicial,
        poblacion_max,
        probabilidad_mutacion,
        longitud
    ]

    guardar(
        '{}.txt'.format(archivos_salida),
        poblacion.registro(),
        parametros_solucion
    )

    serializar('{}.gil'.format(archivos_salida), poblacion.log)


if __name__ == '__main__':
    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    # Si los parametros obligatorios no existen, lanza una excepcion.
    if con_args.dir_archivo is None or con_args.peso_max is None:
        raise Exception(
            'Parametros incompletos, ingresa --help para mostrar la ayuda.'
        )

    # Pasamos los parametros al main.
    main(con_args)