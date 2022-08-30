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
import sys
import csv
import random
import argparse

# Librerias de terceros.
import pandas as pd

# Librerias propias.
from util.plot import graficar_arbol_decision
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

    args_parser.add_argument(
        '--split',
        default=0.6,
        help='Split del dataset para los test y el train',
        dest='split_dataset',
        type=float,
    )

    args_parser.add_argument(
        '--save',
        default=False,
        help='Indica si el modelo se guardara',
        dest='save_model',
        type=bool,
    )

    args_parser.add_argument(
        '--load',
        default=None,
        help='Indica si se cargara el modelo',
        dest='load_model',
        type=str,
    )

    args = args_parser.parse_args()

    return args


def main(con_args: argparse.Namespace, *args, **kargs) -> None:
    # Cargamos los parametros pasados por consola.
    nombre_archivo: str = con_args.nombre_archivo
    atributo_meta: str = con_args.atributo_meta
    split_dataset: float = con_args.split_dataset

    save_model: bool = con_args.save_model
    load_model: str = con_args.load_model

    nombre_salida = nombre_archivo.split('.')[0]

    # Cargamos las instancias del archivo csv.
    print('---> Cargando instancia {}'.format(nombre_archivo))
    dataset = pd.read_csv(nombre_archivo)
    print('---> Instancia Cargada, total de datos cargados {}'.format(
        len(dataset)
    ))
    print(dataset)
    print('\n')

    # Instanciamos el objeto arbol que contiene el modelo.
    modelo = Arbol_Decision(dataset, atributo_meta)

    if load_model is None:
        # Iniciamos el proceso de entrenamiento del arbol de decision.
        modelo.entrenar_modelo(split_dataset)

        if save_model:
            print('---> Modelo guardado')
            modelo.save_modelo(nombre_salida)

    else:
        # Cargamos un modelo.
        print('---> Modelo cargado')
        modelo.load_modelo(load_model)

    print(modelo)

    graficar_arbol_decision(
        modelo,
        nombre_salida
    )

    '''
    # Generamos un input de prueba aleatorio.
    valores_esperados = {
        'Alt': ['Si', 'No'],
        'Bar': ['Si', 'No'],
        'Vier': ['Si', 'No'],
        'Ham': ['Si', 'No'],
        'Clientes': ['Algunos', 'Lleno', 'Ninguno'],
        'Precio': ['$', '$$', '$$$'],
        'Llov': ['Si', 'No'],
        'Res': ['Si', 'No'],
        'Tipo': ['Frances', 'Tailandes', 'Hamburg.', 'Italiano'],
        'Est': ['0-10', '30-60', '10-30', '>60']
    }

    instancia = {}
    for atr in valores_esperados:
        instancia[atr] = random.choice(valores_esperados[atr])

    print('realizando prediccion de {}'.format(instancia))

    prediccion = modelo.realizar_prediccion(
        instancia,
    )

    print('{} predecida {}'.format(atributo_meta, prediccion))
    '''


if __name__ == '__main__':
    # Limpiamos la consola.
    os.system('clear')

    # Establecemos el limite de llamadas recursivas a 2000
    sys.setrecursionlimit(5214)

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
