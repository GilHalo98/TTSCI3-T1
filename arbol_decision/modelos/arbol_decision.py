'''
    Arbol de Decision usando el modelo del arbol de decision
    este modelo es parte del machine learning usando un metodo
    supervisado.

    Este modelo da como salida valores discretos o cualitativos.
'''


# Librerias estandar.
import copy
import fractions
from collections import deque as Pila

# Libreris de terceros.
import pandas as pd
import numpy as np

# Librerias Propias
from util.entropy import I, H
from estructuras_datos.arbol import Arbol


class Arbol_Decision():
    def __init__(
        self,
        dataset: pd.DataFrame,
        atributo_meta: str,
    ) -> None:
        # Dataset del modelo.
        self.dataset = dataset

        # Atributo meta del arbol de Decision.
        self.atributo_meta = atributo_meta

        # Generador de id's para segmetnacion de dataset.
        self.get_id = self.__asignar_id_segmento()

    def __asignar_id_segmento(self) -> str:
        '''
            Se asigna un id para la segmentacion de datos.
        '''

        conteo_id = 0
        while True:
            yield 'S{}'.format(conteo_id)
            conteo_id += 1

    def __calcular_entropias_atributo(
        self,
        dataframe_pivote: pd.DataFrame,
        dataframe_meta: pd.DataFrame
    ) -> pd.Series:
        '''
            Calcula la entropia de un atributo pivote sobre un
            atributo meta.
        '''

        # Se realiza el conteo de los valores del atributo pivote.
        conteo_valores_pivote = dataframe_pivote.value_counts()

        # Se realiza el conteo de los valores del atributo meta.
        conteo_valores_meta = dataframe_meta.value_counts()

        # Se Calcula el todal de datos del dataset.
        total_datos = sum(conteo_valores_pivote)

        # Para calcular la ganancia primero se calcula la probabilidad
        # de los valores del atributo privote.
        probabilidades_valores_pivote = copy.deepcopy(conteo_valores_pivote)
        probabilidades_valores_pivote /= total_datos

        # Generamos un dataframe que contenga el conteo de los valores
        # del pivote relativo al atributo meta.
        conteos = {}

        for valor_pivote in conteo_valores_pivote.keys():
            conteos[valor_pivote] = 0

        dataframe_conteos = pd.DataFrame(
            conteos,
            index=conteo_valores_meta.keys(),
            dtype=np.int64
        )

        # Generamos un dataframe que contenga la entropia de los valores
        # del atributo pivote, este valor tambien es usado para
        # saber su pureza.
        series_entropias = pd.Series(
            conteos.values(),
            index=conteos.keys(),
            dtype=np.float64
        )

        # Realizamos el conteo de valores del atributo pivote en
        # relacion con el atributo meta.
        for valor_pivote, valor_meta in zip(dataframe_pivote, dataframe_meta):
            dataframe_conteos[valor_pivote][valor_meta] += 1

        # Ahora se calcula la entropia del atributo pivote con respecto
        # al atributo meta.
        for valor_pivote in dataframe_conteos:
            total_valores = sum(dataframe_conteos[valor_pivote])

            He_total = 0.0
            for valor_meta in dataframe_conteos[valor_pivote].keys():
                conteo = dataframe_conteos[valor_pivote][valor_meta]

                prob_meta = conteo / total_valores

                informacion_mutua = I(prob_meta, 2)
                He_total += H(prob_meta, informacion_mutua)

            prob_pivote = conteo_valores_pivote[valor_pivote] / total_datos
            series_entropias[valor_pivote] = prob_pivote * He_total

        return series_entropias

    def __ganancia(
        self,
        dataframe_pivote: pd.DataFrame,
        dataframe_meta: pd.DataFrame
    ) -> float:
        '''
            Funcion de ganancia del atributo pivote.
        '''

        # Se calcula la entropia del atributo pivote en referencia del
        # atributo meta.
        series_entropias = self.__calcular_entropias_atributo(
            dataframe_pivote,
            dataframe_meta
        )

        return 1 - sum(series_entropias)

    def __get_atributo_discriminante(
        self,
        dataset: pd.DataFrame,
        dataframe_meta: pd.DataFrame,
    ) -> 'tuple[pd.DataFrame, np.float64]':
        '''
            Funcion move de la heuristica constructiva que selecciona el
            atributo que mas discrimina el atributo meta.
        '''
        mejor_atributo = None
        mejor_ganancia = 0

        for atributo in dataset:
            # Instancia del dataframe del atributo.
            dataframe_atributo = dataset[atributo]

            # Calculamos la ganancia del atributo, esta funcion
            # corresponde a la funcion heurtistica.
            ganancia = self.__ganancia(dataframe_atributo, dataframe_meta)

            # Seleccionamos el mejor atributo que discrimine al
            # atributo meta.
            if ganancia > mejor_ganancia or mejor_atributo is None:
                mejor_atributo = dataframe_atributo
                mejor_ganancia = ganancia

        return mejor_atributo, mejor_ganancia

    def __segmentar_dataset(
        self,
        dataset: pd.DataFrame,
        dataframe_meta: pd.DataFrame,
        pila_segmentacion: Pila,
        id_padre: str = None,
        pureza: np.float64 = 0.0
    ) -> None:
        '''
            Segmenta un dataset dado en multiples sub-sets, la
            segmentacion utiliza un atributo pivote sobre el cual se
            realizara la separacion de los datos, este atributo pivote
            es seleccionado a partir de una medida de ganancia.
        '''
        # Generamos el id de la segmentacion.
        id_segmento = self.get_id.__next__()

        # Se instancia un item de segmentacion para agregarlo a la pila
        # de segentacion.
        item_segmentacion = {
            'id_padre': id_padre,
            'id_segmento': id_segmento
        }

        # Si la pureza es distinta de 1.
        if pureza < 1:
            # El primer paso para para poder seccionar el dataset es
            # encontrar el atributo discriminante.
            dataframe_pivote, ganancia = self.__get_atributo_discriminante(
                dataset,
                dataframe_meta
            )

            # Recuperamos el nombre del atributo pivote.
            atributo_pivote = dataframe_pivote.name

            # Enumeramos los valores del atributo pivote.
            valores_pivote = dataframe_pivote.value_counts().keys()

            # Combinamos el dataset con el dataframe del atributo meta.
            auxiliar_dataset = copy.deepcopy(dataset)
            auxiliar_dataset[self.atributo_meta] = dataframe_meta.values

            # Si la hoja es impura, se agrega la sentencia de seleccion.
            item_segmentacion['sentencia'] = atributo_pivote

            # Lo siguente es segmentar los datos como tal.
            for valor_pivote in valores_pivote:
                # Se realiza la segmentacion del dataset.
                segmentacion = auxiliar_dataset.loc[
                    dataset[atributo_pivote] == valor_pivote
                ]

                # Separamos el atributo meta de los demas atributos
                segmento_dataframe_meta = segmentacion[self.atributo_meta]
                segmento_dataset = segmentacion.drop(
                    self.atributo_meta,
                    axis=1
                )

                # Calculamos la pureza del valor de la segmentacion.
                pureza_valor = 1 - self.__calcular_entropias_atributo(
                    segmento_dataset[atributo_pivote],
                    segmento_dataframe_meta
                )[0]

                # Recursamos la funcion con el segmento de datos.
                self.__segmentar_dataset(
                    segmento_dataset,
                    segmento_dataframe_meta,
                    pila_segmentacion,
                    id_segmento,
                    pureza_valor
                )

        else:
            pass

        pila_segmentacion.append(item_segmentacion)

    def __ensamblar_arbol(self) -> None:
        '''
            Ensambla los arboles de decision dado una pila o historial
            de segmentacion, esta pila contiene elementos con
            la informacion necesaria para generar sub-arboles.
        '''
        pass

    def entrenar_modelo(self) -> None:
        '''
            Genera el modelo del arbol de decision.
        '''

        # Verificamos que el dataset no este vacio.
        if len(self.dataset) <= 0:
            raise Exception('Dataset vacio!')

        # Separamos el atributo meta de los demas atributos
        dataframe_meta = self.dataset[self.atributo_meta]
        dataset = self.dataset.drop(self.atributo_meta, axis=1)

        # Verificamos que la candiad de valores en el atributo meta sea
        # mayor que 1.
        conteo_valores_meta = dataframe_meta.value_counts()
        if len(conteo_valores_meta) < 2:
            return "Todos los elementos pertenecen a {}".format(
                conteo_valores_meta.keys()[0]
            )

        # Instanciamos una pila que almacenara el orden en el cual se
        # recursa la segmentacion de datos, esto para ensamblar el
        # arbol de decision.
        pila_segmentacion = Pila()

        # Ahora se llamara el procedimiento de segmentacion de datos.
        self.__segmentar_dataset(
            dataset,
            dataframe_meta,
            pila_segmentacion
        )

        print('\n')
        while len(pila_segmentacion) > 0:
            print(pila_segmentacion.pop())

        # Ahora se ensamblara el arbol de decision a partir de la
        # pila de segmentacion del dataset.
        self.__ensamblar_arbol()
