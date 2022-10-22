'''
    Algoritmos genericos para resolver el problema de la mochila.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "Diego Gil"


# Librerias estandar.
from re import I
import sys
import pickle
import argparse

# Librerias de terceros.
from matplotlib import pyplot as plt


# Formatea los argumentos pasados por consola.
def format_args():
    args_parser = argparse.ArgumentParser(
        description='Graficador del archivo resultado'
    )

    args_parser.add_argument(
        '--instancia',
        default=None,
        help='Directorio o nombre del archivo resultado, es un archivo .gil',
        dest='dir_archivo',
        type=str,
    )

    args = args_parser.parse_args()

    return args


# Carga el problema del archivo csv.
def cargar(dir_archivo):
    with open(dir_archivo, 'rb+') as archivo:
        return pickle.load(archivo)


# Funcion main.
def main(con_args, *args, **kargs):
    dir_archivo = con_args.dir_archivo
    log = cargar(dir_archivo)

    # Consulta las generaciones generadas del log.
    generaciones = list(log.keys())

    # Consulta los registros del log.
    registros = list(log[generaciones[0]].keys())[:-1]

    datos = {}

    for registro in registros:
        datos[registro] = []

        for generacion in generaciones:
            dato = log[generacion][registro]
            datos[registro].append(dato)

    # Generamos las graficas por cada registro en funcion de la generacion.
    figura, axis = plt.subplots(nrows=3, ncols=2, constrained_layout=False)

    index = 0
    for registro in datos:
        ax = axis.flat[index]
        ax.grid(True)
        ax.bar(generaciones, datos[registro])
        ax.set_title(registro, fontsize=10)
        index += 1

    # Graficamos los individuos de todas las generaciones en peso vs valor.
    individuos_registrados = []
    format_x = []
    format_y = []

    for generacion in generaciones:
        for individuo in log[generacion]['poblacion']:
            id_individuo = individuo['id']

            if id_individuo not in individuos_registrados:
                individuos_registrados.append(id_individuo)

                format_x.append(individuo['peso total'])
                format_y.append(individuo['valor total'])

    ax = axis.flat[-1]
    ax.grid(True)
    ax.plot(format_x, format_y, 'o')
    ax.set_title('Poblacion', fontsize=10)

    plt.show()


if __name__ == '__main__':
    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    # Si los parametros obligatorios no existen, lanza una excepcion.
    if con_args.dir_archivo is None:
        raise Exception(
            'Parametros incompletos, ingresa --help para mostrar la ayuda.'
        )

    # Pasamos los parametros al main.
    main(con_args)