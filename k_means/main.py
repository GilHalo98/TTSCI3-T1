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
import argparse

# Librerias de terceros.
import pandas as pd
import seaborn as sb
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

# Formatea los argumentos pasados por consola.
def format_args() -> argparse.Namespace:
    args_parser = argparse.ArgumentParser(
        description='Genera un arbol de decision dado un archivo CSV'
    )

    args_parser.add_argument(
        '--dataset',
        default=None,
        help='Nombre del archivo del dataset',
        dest='nombre_archivo',
        type=str,
    )

    args_parser.add_argument(
        '--atr_obj',
        default=None,
        help='Nombre del atributo objetivo',
        dest='atr_obj',
        type=str,
    )

    args = args_parser.parse_args()

    return args


def main(con_args: argparse.Namespace, *args, **kargs) -> None:
    # Cargamos los parametros pasados por consola.
    nombre_archivo: str = con_args.nombre_archivo
    atr_obj: str = con_args.atr_obj

    # Cargamos el dataset.
    dataset = pd.read_csv(nombre_archivo)

    print('---> Dataset Cargado')
    print(dataset)
    print(dataset.describe())

    # Eliminamos los datos que son invalidos.
    dataset = dataset.dropna()

    # Mostramos un historico de los datos.
    print('---> Graficando historico')
    dataset.hist()
    plt.show()

    # Eliminamos el atributo objetivo del dataset.
    #dataset = dataset.drop([atr_obj], 1)

    # Generamos el grafico de los atributos con mayor relacion.
    sb.pairplot(
        dataset,
        hue=atr_obj,
        height=4,
        vars=['chlorides', 'density', 'volatile acidity'],
        kind='scatter'
    )
    plt.show()

    print('---> Particionando los datos.')
    X = np.array(dataset[['chlorides', 'density', 'volatile acidity']])
    y = np.array(dataset[atr_obj])

    X.shape

    fig = plt.figure()
    ax = Axes3D(fig)
    colores=[
        'blue',
        'red',
        'green',
        'blue',
        'cyan',
        'yellow',
        'orange',
        'black',
        'pink',
        'brown',
        'purple'
    ]
    asignar=[]
    for row in y:
        asignar.append(colores[row])
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=asignar, s=60)
    plt.show()

    print('---> Calculando valor optimo para K')
    Nc = range(1, 20)
    kmeans = [
        KMeans(n_clusters=i) for i in Nc
    ]

    score = [
        kmeans[i].fit(X).score(X) for i in range(len(kmeans))
    ]

    plt.plot(Nc, score)
    plt.xlabel('K')
    plt.ylabel('Aptitud')
    plt.title('Curva de codo')
    plt.show()

    print('---> Realizando entrenamiento del modelo')
    kmeans = KMeans(n_clusters=5).fit(X)
    centroids = kmeans.cluster_centers_
    print('---> Centroides')
    print(centroids)

    # Realizamos predicciones.
    labels = kmeans.predict(X)

    # Identificamos los centroides.
    C = kmeans.cluster_centers_
    colores=['red', 'green', 'blue', 'cyan', 'yellow']
    asignar=[]
    for row in labels:
        asignar.append(colores[row])

    fig_2 = plt.figure()
    ax = Axes3D(fig_2)
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=asignar, s=60)
    ax.scatter(C[:, 0], C[:, 1], C[:, 2], marker='*', c=colores, s=1000)
    plt.show()


if __name__ == '__main__':
    # Limpiamos la consola.
    os.system('clear')

    # Formateamos los parametros pasados por consola.
    con_args = format_args()

    if con_args.nombre_archivo is None or con_args.atr_obj is None:
        mensaje = 'Es necesario llenar todos los parametros'
        mensaje += ', usa -h para mostrar la ayuda'

        raise Exception(
            mensaje
        )

    # Ejecutamo la funcion main.
    main(con_args)
