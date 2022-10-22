'''
    Algoritmo para el entrenamiento de una SVM.
'''

# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
__author__ = "Diego Gil"


# Librerias estandar.
import os
import argparse

# Librerias de terceros.
import pandas as pd
import seaborn as sb
import numpy as np
from matplotlib import pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

# Formatea los argumentos pasados por consola.
def format_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(
        description='Genera una SVM dado un archivo CSV'
    )

    args_parser.add_argument(
        '--dataset',
        default=None,
        help='Nombre del archivo del dataset',
        dest='nombre_archivo',
        type=str,
    )

    args_parser.add_argument(
        '--val_dep',
        default=None,
        help='Nombre del atributo dependiente (F)',
        dest='val_dep',
        type=str,
    )

    args = args_parser.parse_args()

    return args


def main(con_args: argparse.Namespace, *args, **kargs) -> None:
    # Cargamos los parametros pasados por consola.
    nombre_archivo: str = con_args.nombre_archivo
    val_dep: str = con_args.val_dep

    # Cargamos el dataset.
    dataset = pd.read_csv(nombre_archivo)

    print('---> Dataset Cargado')
    print(dataset)
    print(dataset.describe())

    # Eliminamos los datos que son invalidos.
    dataset = dataset.dropna()

    # Indicamos que propiedades seran usadas como variables dependientes.
    X = dataset.drop(columns=val_dep)
    y = dataset[val_dep]

    # Realizamos la particion de datos de entrenamiento y de pruebas.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        train_size=0.8,
        random_state=1234,
        shuffle=True
    )

    # Creamos el modelo.
    modelo = SVC(C=100, kernel='linear', random_state=123)

    # Realizamos el entrenamiento.
    modelo.fit(X_train, y_train)

    # Realizamos las predicciones con el set de test.
    predicciones = modelo.predict(X_test)

    # Calculamos la certeza del modelo.
    certeza = accuracy_score(y_true=y_test, y_pred=predicciones, normalize=True)

    print('---> El modelo tiene una certeza del {0:.2f}%'.format(certeza*100))

if __name__ == '__main__':
    # Limpiamos la consola.
    os.system('clear')

    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    if (
        con_args.nombre_archivo is None
        or con_args.val_dep is None
    ):
        mensaje = 'Es necesario llenar todos los parametros'
        mensaje += ', usa -h para mostrar la ayuda'

        raise Exception(
            mensaje
        )

    # Ejecutamo la funcion main.
    main(con_args)
