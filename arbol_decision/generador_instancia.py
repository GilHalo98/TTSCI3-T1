'''
    Generador de instancias para el programa de arboles de decisión,
    genera un archivo .csv el cual contiene los items de la instancia.
'''


# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "Diego Gil"


# Librerias estandar.
import os
import csv
import random
import argparse

# Librerias de terceros.
from progress.bar import ChargingBar as Barra


# Formatea los argumentos pasados por consola.
def format_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(
        description='''
        Genera una instancia para el programe del arbol
        de decisión, el formato tomado es en csv
        '''
    )

    args_parser.add_argument(
        '--nombre_salida',
        default=None,
        help='Nombre del archivo de salida',
        dest='nombre_archivo',
        type=str,
    )

    args_parser.add_argument(
        '--num_elementos',
        default=10,
        help='Total de items en la instancia',
        dest='numero_items',
        type=int
    )

    args = args_parser.parse_args()

    return args


def main(con_args: argparse.Namespace, *args, **kargs) -> None:
    # Cargamos los parametros pasados por consola.
    nombre_archivo: str = con_args.nombre_archivo
    numero_items: int = con_args.numero_items

    valores_esperados = {
        'Alt': {
            'Si': 0.7,
            'No': 0.3
        },
        'Bar': {
            'Si': 0.6,
            'No': 0.2
        },
        'Vier': {
            'Si': 0.5,
            'No': 0.5
        },
        'Ham': {
            'Si': 0.8,
            'No': 0.2
        },
        'Clientes': {
            'Algunos': 0.5,
            'Lleno': 0.2,
            'Ninguno': 0.3
        },
        'Precio': {
            '$': 0.5,
            '$$': 0.3,
            '$$$': 0.2
        },
        'Llov': {
            'Si': 0.5,
            'No': 0.5
        },
        'Res': {
            'Si': 0.6,
            'No': 0.4
        },
        'Tipo': {
            'Frances': 0.2,
            'Tailandes': 0.2,
            'Hamburg.': 0.5,
            'Italiano': 0.1
        },
        'Est': {
            '0-10': 0.4,
            '10-30': 0.3,
            '30-60': 0.2,
            '>60': 0.1
        },
        'Esperar': {
            'Si': 0.4,
            'No': 0.6
        }
    }

    instancias = []

    with open('{}.csv'.format(nombre_archivo), 'w+') as obj_csv:
        atributos = list(valores_esperados.keys())
        cabezal = csv.DictWriter(obj_csv, fieldnames=atributos)
        cabezal.writeheader()

        barra_progreso = Barra('-----> Generando elementos', max=numero_items)

        while numero_items > 0:
            instancia = {}

            for atr in valores_esperados:
                instancia[atr] = random.choices(
                    list(valores_esperados[atr].keys()),
                    list(valores_esperados[atr].values())
                )[0]

            instancias.append(instancia)
            cabezal.writerow(instancia)
            barra_progreso.next()
            numero_items -= 1

        barra_progreso.finish()
        
        print('-----> Elementos generados, guardando en archivo {}.csv'.format(
            nombre_archivo
        ))


if __name__ == '__main__':
    # Limpiamos la consola.
    os.system('clear')

    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    if con_args.nombre_archivo is None:
        mensaje = 'Es necesario llenar todos los parametros'
        mensaje += ', usa -h para mostrar la ayuda'

        raise Exception(
            mensaje
        )

    # Ejecutamo la funcion main.
    main(con_args)