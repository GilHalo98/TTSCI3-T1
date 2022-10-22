'''
    Algoritmos genericos para resolver el problema de la mochila.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "Diego Gil"


# Librerias estandar.
import argparse
import csv
from random import randint


# Formatea los argumentos pasados por consola.
def format_args():
    args_parser = argparse.ArgumentParser(
        description='Problema de la mochila resuelto con algoritmos geneticos'
    )

    args_parser.add_argument(
        '--archivoSalida',
        default=None,
        help='Nombre del archivo saida',
        dest='archivo_salida',
        type=str,
    )

    args_parser.add_argument(
        '--totalItems',
        default=None,
        help='Total de items en la mochila',
        dest='total_items',
        type=int,
    )

    args_parser.add_argument(
        '--pesoMinimo',
        default=10,
        help='Peso minimo que se puede generar',
        dest='peso_min',
        type=int,
    )

    args_parser.add_argument(
        '--pesoMaximo',
        default=100,
        help='Peso maximo que se puede generar',
        dest='peso_max',
        type=int,
    )

    args_parser.add_argument(
        '--valorMinimo',
        default=10,
        help='Valor minimo que se puede generar',
        dest='valor_min',
        type=int,
    )

    args_parser.add_argument(
        '--valorMaximo',
        default=100,
        help='Valor maximo que se puede generar',
        dest='valor_max',
        type=int,
    )

    args = args_parser.parse_args()

    return args


# Guarda el problema en un archivo csv.
# Carga el problema del archivo csv.
def guardar_problema(dir_archivo, datos, total_datos):
    with open(dir_archivo, 'w+', newline='') as archivo:
        propiedades = list(datos.keys())
        objeto_archivo = csv.DictWriter(archivo, fieldnames=propiedades)

        # Escribe la cabecera en el archivo csv.
        objeto_archivo.writeheader()

        # Guardamos los datos en el archivo.
        for index in range(total_datos):
            registro = {}

            for propiedad in propiedades:
                registro[propiedad] = datos[propiedad][index]

            objeto_archivo.writerow(registro)


# Funcion main.
def main(con_args, *args, **kargs):
    dir_archivo = con_args.archivo_salida
    total_items = con_args.total_items
    peso_min = con_args.peso_min
    peso_max = con_args.peso_max
    valor_min = con_args.valor_min
    valor_max = con_args.valor_max

    problema = {
        'peso': [],
        'valor': []
    }

    for _ in range(total_items):
        problema['peso'].append(randint(peso_min, peso_max))
        problema['valor'].append(randint(valor_min, valor_max))

    guardar_problema(dir_archivo, problema, total_items)


if __name__ == '__main__':
    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    # Si los parametros obligatorios no existen, lanza una excepcion.
    if con_args.archivo_salida is None or con_args.total_items is None:
        raise Exception(
            'Parametros incompletos, ingresa --help para mostrar la ayuda.'
        )

    # Pasamos los parametros al main.
    main(con_args)