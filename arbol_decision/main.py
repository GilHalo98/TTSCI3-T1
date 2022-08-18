# -*- coding: utf-8 -*-

from os import system
from csv import reader
from fractions import Fraction

from entropy import probabilidades, I, H

# Instancia a cargar.
archivo_instancia = 'instancia_prueba.csv'
atributo_meta = 'Esperar'


def cargar_instancias(filedir):
    # Se carga la instancia desde un archivo csv y se
    # pasa a un formato dict.
    instancias = {}
    total_instancias = 0
    with open(filedir, 'r+') as obj_csv:
        cabezal = reader(obj_csv)
        atributos = next(cabezal)

        for atributo in atributos:
            instancias[atributo] = []

        for linea in cabezal:
            instancia = {}

            for atributo, valor in zip(atributos, linea):
                instancias[atributo].append(valor)

            total_instancias += 1

    return instancias, total_instancias


def enumerar_valores(atributo, dataset):
    # Enumera los posibles valores de un atributo.
    valores = []

    for valor in dataset[atributo]:
        if valor not in valores:
            valores.append(valor)

    return valores


def contar_todo(datos_atributo):
    # Cuenta las instancias por valor de atributo.
    conteo = {}
    for dato in datos_atributo:
        if dato in conteo:
            conteo[dato] += 1

        else:
            conteo[dato] = 1
    return conteo


def contar_contra_meta(
    atributo,
    posibles_valores,
    posibles_valores_meta,
    long_dataset,
    dataset
):
    # Contar los valores positivos y negatios por atributos contra el
    # atributo meta. retorna el conteo para poder calcular la entropia
    # del atributo para verificar si es un buen atributo o un
    # atributo invalido.
    conteos = {}

    # Por cada posible valor en el atributo.
    for posible_valor in posibles_valores:
        conteo = {}
        
        # Inicializamos los conteos en 0 de los valores relativos
        # al atributo meta.
        for posible_valor_meta in posibles_valores_meta:
            conteo[posible_valor_meta] = 0

        conteos[posible_valor] = conteo

    # Empezamos a realizar el conteo.
    for index in range(long_dataset):
        valor_atributo = dataset[atributo][index]
        valor_meta = dataset[atributo_meta][index]

        conteos[valor_atributo][valor_meta] += 1

    return conteos


def constructive_heuristic():
    # Heuristica constructiva del algoritmo de creacion de arboles.
    pass


def heuristica():
    # Heuristica, usa la entropia entre el atributo test y el
    # atributo meta para poder calcular una ganancia.
    ganancia = 0
    return ganancia


def main():
    # Cargamos las instancias del archivo csv.
    print('Cargando instancias...')
    dataset, long_dataset = cargar_instancias(archivo_instancia)

    print('{} instancias cargadas'.format(long_dataset))
    conteo_atributos_meta = contar_todo(dataset[atributo_meta])

    # Enumeramos los posibles valores del atributo meta.
    posibles_valores_meta = enumerar_valores(atributo_meta, dataset)


    # Calculamos cual es el mejor atributo.
    print('Construyendo el arbol de decision')

    # Por cada atributo en el dataset.
    for atributo in dataset:

        # Excluyendo el atributo meta.
        if atributo != atributo_meta:
            # Enumeramos los posibles valores para el atributo.
            posibles_valores = enumerar_valores(atributo, dataset)
            print('\tatributo: {}, posibles valores: {}'.format(
                atributo,
                posibles_valores
            ))

            # Contamos la ocurrencia del valor sobre el atributo.
            conteo = contar_todo(dataset[atributo])

            print('\tconteo de valores del atributo: {}'.format(conteo))

            # Contamos la ocurrencia de los posibles valores de los
            # atributos y sus valores en el estado meta,
            # positivos y negativos.
            conteo_meta = contar_contra_meta(
                atributo,
                posibles_valores,
                posibles_valores_meta,
                long_dataset,
                dataset
            )

            print('\tconteo contra meta: {}'.format(conteo_meta))

            # Calculamos las probabilidades de la informacion de los atributos
            # en referencia al atributo meta.
            probabilidades_meta = {}

            for valor in posibles_valores:
                probabilidades_meta[valor] = probabilidades(conteo_meta[valor])

            print('\tProbabilidades contra meta: {}'.format(probabilidades_meta))

            # Ahora se utiliza una heuristica constructiva Best-Found
            # con funcion greedy h(i) = 1 - H(Ei) para indicar cual
            # es el mejor atributo para realizar el arbol.

            # Determinamos la base del logaritmo para utilizar.
            base_log = 2 # if len(conteo) <= 2 else 10
            print('\tBase logaritmica a usar: {}'.format(base_log))

            # Calculamos las probabilidades dado el conteo de los
            # valores del atributo.
            prob = probabilidades(conteo)

            # Calculamos la informacion mutua o sorpresa del valor
            # del atributo.
            H_valor = 0
            for valor in probabilidades_meta:
                # Obtenemos la probabilidad del valor respecto a su
                # atributo.
                prob_valor = prob[valor]

                # Primero calculamos la entropia de cada valor relativo
                # al atributo meta por separado.
                He = 0
                for valor_meta in probabilidades_meta[valor]:
                    prob__valor_meta = probabilidades_meta[valor][valor_meta]
                    I_valor_meta = I(prob__valor_meta, 2)
                    He += H(prob__valor_meta, I_valor_meta)
                print('\tValor: ', valor, '{} * {} = {}'.format(
                    prob_valor,
                    He,
                    prob_valor * He
                ))
                H_valor += prob_valor * He

            ganancia = 1 - H_valor

            print('\tGanancia({}) = {}'.format(atributo, ganancia))

            print('-'*100)
    '''

    # Se calcula la ganancia de la informacion por
    # atributo.
    mejor_atr = None
    mejor_ganancia = None

    for atributo in instancias:
        # Mientras que el atributo sea distinto
        # al atributo meta.
        if atributo != atributo_meta:
            print('Atributo: {}'.format(atributo))
            conteo = contar_todo(instancias[atributo])
            print('Conteo ocurrencias de valores en atributo: {}'.format(
                conteo
            ))
            prob = probabilidades(conteo)
            print('Probabilidades por atributo: {}'.format(prob))
            base = 2 if len(conteo) <= 2 else 10
            print('base usada: {}'.format(base))

            conteo_atr_meta = contar_contra_meta(
                instancias,
                atributo,
                conteo,
                conteo_atributos_meta,
                total_instancias
            )

            print('Conteo de ocurrencias contra meta: {}'.format(
                conteo_atr_meta
            ))

            h = H(*list(prob.values()), base=base)
            ganancia = 1 - sum(h)
            print('Ganancia: {0:.6f}'.format(ganancia))
            print('-'*50)

            if mejor_atr is not None:
                if ganancia > mejor_ganancia:
                    mejor_atr = atributo
                    mejor_ganancia = ganancia

            else:
                mejor_atr = atributo
                mejor_ganancia = ganancia

    print('mejor atr {} mejor ganancia {}'.format(
        mejor_atr,
        mejor_ganancia
    ))
    '''


if __name__ == '__main__':
    system('clear')
    main()
