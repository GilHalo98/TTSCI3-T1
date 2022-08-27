'''
    Algoritmo para el entrenamiento de un arbol de decision.
    se utiliza la clase arbol de clasificacion para poder hacer
    uso de sus propiedades, asi como de efectuar el entrenamiento y una
    prediccion.
'''

# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "Diego Gil"


# Librerias estandar.
import os
import csv
import argparse

# Librerias de terceros.
import pandas as pd

# Librerias propias.
from util.entropy import probabilidades, I, H
from modelos.arbol_decision import Arbol_Decision


# Formatea los argumentos pasados por consola.
def format_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(
        description='Genera un arbol de decision dado un archivo CSV'
    )

    args_parser.add_argument(
        '--instancia',
        default=None,
        help='Nombre del archivo de la instancia',
        dest='nombre_archivo',
        type=str,
    )

    args_parser.add_argument(
        '--atr_meta',
        default=None,
        help='Nombre del atributo meta del modelo',
        dest='atributo_meta',
        type=str,
    )

    args = args_parser.parse_args()

    return args


def main(con_args: argparse.Namespace, *args, **kargs) -> None:
    # Cargamos los parametros pasados por consola.
    nombre_archivo: str = con_args.nombre_archivo
    atributo_meta: str = con_args.atributo_meta

    # Cargamos las instancias del archivo csv.
    print('Cargando instancias...')
    dataset = pd.read_csv(nombre_archivo)
    print('Instancias Cargadas, total de datos cargados {}'.format(
        len(dataset)
    ))
    print(dataset)

    # Instanciamos el objeto arbol que contiene el modelo.
    modelo = Arbol_Decision(dataset, atributo_meta)

    # Iniciamos el proceso de entrenamiento del arbol de decision.
    modelo.entrenar_modelo()


if __name__ == '__main__':
    # Limpiamos la consola.
    os.system('clear')

    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    if con_args.nombre_archivo is None or con_args.atributo_meta is None:
        mensaje = 'Es necesario llenar todos los parametros'
        mensaje += ', usa -h para mostrar la ayuda'

        raise Exception(
            mensaje
        )

    # Ejecutamo la funcion main.
    main(con_args)
