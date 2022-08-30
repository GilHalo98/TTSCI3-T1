'''
    Arbol de Decision usando el modelo del arbol de decision
    este modelo es parte del machine learning usando un metodo
    supervisado.

    Este modelo da como salida valores discretos o cualitativos.
'''


# Librerias estandar.
import sys
import copy
import pickle
from collections import deque as Pila

# Libreris de terceros.
import numpy as np
import pandas as pd
from progress.spinner import PixelSpinner as Spinner
from progress.bar import ChargingBar as Barra

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

        # Estructura de datos que mantiene los nodos del arbol 
        # de decision.
        self.__arbol = Arbol()

        # Spinner del segmentador de datos.
        self.__spinner = Barra(
            max=sys.getrecursionlimit(),
            suffix='Nivel de recurción: %(index)d de %(max)d'
        )

        # Barra del ensamblado del arbol.
        self.__barra = Barra()

        # Barra de la evaluacion del modelo.
        self.__barra_evaluacion = Barra()

    def __str__(self) -> str:
        '''
            Representacion en str del arbol de decision.
        '''
        representacion = ''

        # Si el arbol estavacio.
        if self.__arbol.esta_vacio():
            representacion += 'Arbol Vacio!'

        # Sino, se generan las reglas logicas.
        else:
            representacion += '\nArbol de decisión como reglas lógicas:\n'
            for id_nodo in self.__arbol:
                nodo = self.__arbol[id_nodo]

                for id_conexion in nodo.conexiones:
                    valor_conexion = nodo.conexiones[id_conexion]

                    nodo_conexion = self.__arbol[id_conexion]

                    sentencia = ''

                    if nodo_conexion.es_hoja():
                        sentencia += 'if {} ({}) is {} then {} is {}'.format(
                            nodo.propiedades['atributo'],
                            nodo.id,
                            nodo.conexiones[id_conexion],
                            self.atributo_meta,
                            nodo_conexion.propiedades['valor_meta']
                        )

                    else:
                        sentencia += 'if {} ({}) is {} then evaluate {} ({})'.format(
                            nodo.propiedades['atributo'],
                            nodo.id,
                            nodo.conexiones[id_conexion],
                            nodo_conexion.propiedades['atributo'],
                            nodo_conexion.id
                        )

                    representacion += sentencia + '\n'

        return representacion

    def __asignar_id_segmento(self) -> str:
        '''
            Se asigna un id para la segmentacion de datos.
        '''

        conteo_id = 0
        while True:
            yield 'N{}'.format(conteo_id)
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
        pureza: np.float64 = 0.0,
        valor_precedente: str = None
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
            'id_segmento': id_segmento,
            'pureza': pureza,
            'cantidad_datos': len(dataset)
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
            item_segmentacion['atributo'] = atributo_pivote

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

                self.__spinner.next()

                # Recursamos la funcion con el segmento de datos.
                self.__segmentar_dataset(
                    segmento_dataset,
                    segmento_dataframe_meta,
                    pila_segmentacion,
                    id_segmento,
                    pureza_valor,
                    valor_pivote
                )

        else:
            # Se almacena el valor final del atributo meta.
            item_segmentacion['valor_meta'] = dataframe_meta.values[0]

        # El valor precedente del atributo pivote se almacena.
        item_segmentacion['valor_precedente'] = valor_precedente

        # Agregamos el item a la pila de segmentacion.
        pila_segmentacion.append(item_segmentacion)

    def __ensamblar_arbol(
        self,
        pila_segmentacion: Pila,
    ) -> None:
        '''
            Ensambla los arboles de decision dado una pila o historial
            de segmentacion, esta pila contiene elementos con
            la informacion necesaria para generar sub-arboles.
        '''
        self.__barra.max = len(pila_segmentacion)
        while len(pila_segmentacion) > 0:
            # Se recupera el item de la pila de segmentacion.
            item_segmento = pila_segmentacion.pop()

            # Recuperamos aquellos valores del item que son parte de
            # los atributos del nodo.
            id_padre = item_segmento['id_padre']
            id_segmento = item_segmento['id_segmento']
            valor_precedente = item_segmento['valor_precedente']

            # Los eliminamos del item.
            del item_segmento['id_padre']
            del item_segmento['id_segmento']
            del item_segmento['valor_precedente']

            # Instanciamos el item en el arbol.
            self.__arbol.inicializar_nodo(
                id_segmento,
                {},
                **item_segmento
            )

            # Identificamos si el item sera asignado como la raiz del
            # arbol.
            if id_padre is None:
                self.__arbol.raiz = id_segmento

            # Si no es el nodo raiz, eso quiere decir que tiene un nodo
            # padre por lo cual se hace la conexion del nodo padre al
            # nodo hijo.
            else:
                self.__arbol.agregar_conexion(
                    id_padre,
                    id_segmento,
                    valor_precedente
                )
            self.__barra.next()

    def __generar_matriz_confucion(
        self,
        valores: 'list[str]',
    ) -> pd.DataFrame:
        template = {}

        valores.append(None)

        for valor in valores:
            template[valor] = [0 for _ in valores]

        return pd.DataFrame(template, index=valores)

    def evaluar_modelo(
        self,
        dataset_test: pd.DataFrame,
        matriz_confucion: pd.DataFrame,
        valores_atributo_meta: str,
    ) -> float:
        '''
            Evalua la calidad del modelo generado.
        '''

        # Realizamos las predicciones con el dataset de test.
        for index in dataset_test.index:
            item = dataset_test.loc[index]
            verdadero = item[self.atributo_meta]

            prediccion = self.realizar_prediccion(item)

            matriz_confucion[prediccion][verdadero] += 1

            self.__barra_evaluacion.next()

        # calculamos la certeza.
        acertados = 0
        for valor_meta in valores_atributo_meta:
            acertados += matriz_confucion[valor_meta][valor_meta]

        certeza = acertados / len(dataset_test)

        return certeza

    def entrenar_modelo(
        self,
        split_dataset_train: float = 0.6,
        seed: int = 201
    ) -> None:
        '''
            Genera el modelo del arbol de decision.
        '''

        # Realizamos un split de los datos para un dataset de
        # entrenamiento y otro de evaluacion.
        print('---> Split del dataset, fracción seleccionada {}'.format(
            split_dataset_train
        ))
        dataset_train = self.dataset.sample(
            frac=split_dataset_train,
            random_state=seed
        )
        dataset_test = self.dataset.drop(dataset_train.index)
        print('---> Elementos en dataset train: {}'.format(len(dataset_train)))
        print('---> Elementos en dataset test: {}\n'.format(len(dataset_test)))

        # Verificamos que el dataset de entrenamiento no este vacio.
        if len(dataset_train) <= 0:
            raise Exception('Dataset vacio!')

        # Separamos el atributo meta de los demas atributos
        dataframe_meta = dataset_train[self.atributo_meta]
        dataset = dataset_train.drop(self.atributo_meta, axis=1)

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
        self.__spinner.message = '---> Segmentación del dataset test'
        self.__spinner.start()
        self.__segmentar_dataset(
            dataset,
            dataframe_meta,
            pila_segmentacion
        )
        self.__spinner.finish()

        # Ahora se ensamblara el arbol de decision a partir de la
        # pila de segmentacion del dataset.
        self.__barra.message = '---> Ensamblado del árbol de decisión'
        self.__barra.start()
        self.__ensamblar_arbol(pila_segmentacion)
        self.__barra.finish()

        # Generamos la matriz de confución del modelo.
        valores_atributo_meta = list(
            self.dataset[self.atributo_meta].value_counts().keys()
        )

        matriz_confucion = self.__generar_matriz_confucion(
            valores_atributo_meta
        )

        print('\n')

        # Por ultimo realizamos la evaluacion del modelo.
        self.__barra_evaluacion.message = '---> Evaluando el modelo'
        self.__barra_evaluacion.max = len(dataset_test)
        self.__barra_evaluacion.start()
        certeza = self.evaluar_modelo(
            dataset_test,
            matriz_confucion,
            valores_atributo_meta
        )
        self.__barra_evaluacion.finish()

        print('---> Certeza del modelo: {}'.format(certeza))
        print('---> Matriz de confucion: \n{}'.format(matriz_confucion))

    def realizar_prediccion(self, input: dict) -> str:
        '''
            Funcion que realiza la predicción de un input con el modelo
            entrenado.
        '''
        nodo = self.__arbol[self.__arbol.raiz]

        while not nodo.es_hoja():
            atributo = nodo.propiedades['atributo']

            encontrado = False
            for id_conexion in nodo.conexiones:
                valor = nodo.conexiones[id_conexion]

                if input[atributo] == valor:
                    nodo = self.__arbol[id_conexion]
                    encontrado = True
                    break

            if not encontrado:
                return None
                break

        return nodo.propiedades['valor_meta']

    def save_modelo(self, nombre_archivo: str) -> None:
        '''
            Guarda en un archivo permanente el modelo.
        '''

        # Abre o crea y abre el archivo y guarda los datos.
        with open('{}.bin'.format(nombre_archivo), 'wb+') as archivo:
            pickle.dump(
                self.__arbol,
                archivo,
                protocol=pickle.HIGHEST_PROTOCOL
            )

    def load_modelo(self, nombre_archivo: str) -> None:
        '''
            Carga un modelo de un archivo permanente.
        '''

        # Carga un archivo y sus datos.
        with open(nombre_archivo, 'rb+') as archivo:
            self.__arbol = pickle.load(archivo)

            print(self.__arbol)

    def get_arbol(self) -> Arbol:
        return self.__arbol