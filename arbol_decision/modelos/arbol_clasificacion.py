'''
    Arbol de clasificacion usando el modelo del arbol de decision
    este modelo es parte del machine learning usando un metodo
    supervisado.

    Este modelo da como salida valores discretos o cualitativos.
'''


# Librerias estandar.
import copy
import fractions


class Arbol_Clasificacion():
    def __init__(
        self,
        dataset: dict,
        atributo_meta: str,
        longitud_dataset: int,
    ) -> None:
        '''
            Dataset de entrenamiento del arbol de clasificacion.

            La estructura del dataset tiene que ser la siguiente:
                Dataset: {
                    atributo_1: [
                        valor_instancia_1,
                        ...,
                        valor_instancia_n
                    ],
                    ...,
                    atributo_n: [
                        valor_instancia_1,
                        ...,
                        valor_instancia_n
                    ]
                }
        '''
        self.dataset = dataset

        # Atributo meta del arbol de clasificacion.
        self.atributo_meta = atributo_meta

        # Tamaño del dataset, que tantas instancias contiene.
        self.longitud_dataset = longitud_dataset

    def __str__(self) -> str:
        '''
            Retorna una representacion str del modelo.
        '''
        return 'arbol de decision'

    def enumerar_valores_atributo(
        self,
        atributo: str,
        dataset: dict
    ) -> 'list[str]':
        # Enumera los posibles valores de un atributo.
        valores = []

        for valor in dataset[atributo]:
            if valor not in valores:
                valores.append(valor)

        return valores

    def contar_valores_atributo(self, datos_atributo) -> dict:
        # Cuenta las instancias por valor de atributo.
        conteo = {}

        for dato in datos_atributo:
            if dato in conteo:
                conteo[dato] += 1

            else:
                conteo[dato] = 1

        return conteo

    def contar_valores_contra_meta(
        self,
        dataset: dict,
        atributo: str,
        valores_atributo_meta: 'list[str]',
        valores_atributo: 'list[str]',
    ) -> None:
        # Contar los valores positivos y negatios por atributos contra el
        # atributo meta. retorna el conteo para poder calcular la entropia
        # del atributo para verificar si es un buen atributo o un
        # atributo invalido.
        conteos = {}

        # Se calcula la longitud de la instancia.
        longitud_dataset = len(list(dataset.values())[0])

        # Poblamos el diccionario de conteos con el valor del atributo
        # y los valores del atributo meta.
        for valor_atributo in valores_atributo:
            conteo = {}

            for valor_meta in valores_atributo_meta:
                conteo[valor_meta] = 0

            conteos[valor_atributo] = conteo

        # Contamos los valores con respecto a los valores de la meta.
        for index in range(longitud_dataset):
            valor_meta = dataset[atributo][index]
            valor_atributo = dataset[self.atributo_meta][index]

            conteos[valor_atributo][valor_meta] += 1

        return conteos

    def probabilidades(data):
        # Calcula la probabilidad de suceso de un evento dado.
        probabilidades = {}
        total = sum(list(data.values()))

        for dato in data:
            probabilidades[dato] = fractions.Fraction(data[dato], total)

        return probabilidades

    def movimiento(
        self,
        dataset_entrenamiento: dict,
        valores_atributo_meta: 'list[str]',
    ) -> None:
        # Funcion movimiento, esta funcion genera un candidato para la
        # heuristica constructiva.
        # Por cada atributo en el dataset.

        for atributo in dataset_entrenamiento:

            # Mientras que el atributo sea distinto al atributo meta.
            if atributo != self.atributo_meta:
                # Enumeramos los posibles valores del atributo.
                posibles_valores_atributo = self.enumerar_valores_atributo(
                    atributo,
                    dataset_entrenamiento
                )

                # Contamos los valores del atributo.
                conteo = self.contar_valores_atributo(
                    dataset_entrenamiento[atributo]
                )

                # Contamos los valores del atributo contra el atributo
                # meta.
                conteo_contra_meta = self.contar_valores_contra_meta(
                    dataset_entrenamiento,
                    atributo,
                    valores_atributo_meta,
                    posibles_valores_atributo,
                )

                print(conteo_contra_meta)

                yield {
                    'atributo': atributo,
                    # 'ganancia': ganancia,
                    # 'hojas': hojas
                }

    def best_found(
        self,
        dataset_entrenamiento: dict,
        valores_atributo_meta: 'list[str]'
    ) -> str:
        # Heuristica contructiva con estrategia best-found.
        mejor_atributo = ''

        # Conteo de los valores del atributo meta.
        conteo_atributos_meta = self.contar_valores_atributo(
            dataset_entrenamiento[self.atributo_meta]
        )

        # Instanciamos el generador de movimientos o candidatos a
        # usar en la heuristica constructiva.
        generar_candidato = self.movimiento(
            dataset_entrenamiento,
            valores_atributo_meta
        )

        # Por cada candidato generado.
        for candidato in generar_candidato:
            print(candidato)

        return mejor_atributo

    def entrenar(self) -> None:
        '''
            Funcion de entrenamiento del arbol de clasificacion.

            - mientras que existan atributos por agregar al arbol:
                - contar los valores que existan en los atributos

                - calcular la probabilidad de los valores de
                    los atributos

                - contar los valores de los atributos con respecto a los
                    valores del atributo meta

                - calcular la probabilidad de los valores del atributo
                    con respecto a los valores del atributo meta

                - calcular la ganancia de los atributos

                - seleccionar el mejor atributo y construir un sub-arbol

                - aquellos valores en grupos puros o hojas puras
                    quitarlos del dataset

                - si existe un atributo que ya no contenga hojas impuras
                    quitarlo del dataset

                - repetir
        '''

        # Se realiza una copia del dataset para el entrenamiento.
        dataset_entrenamiento = copy.deepcopy(self.dataset)

        # Enumeramos los posibles valores del atributo meta.
        posibles_valores_meta = self.enumerar_valores_atributo(
            self.atributo_meta,
            dataset_entrenamiento
        )

        # Mientras que existan atributos por agregar al arbol.
        while len(dataset_entrenamiento) > 1:
            # Encuentra el mejor atributo
            mejor_atributo = self.best_found(
                dataset_entrenamiento,
                posibles_valores_meta
            )

            # Genera un sub-arbol

            # Si el atributo seleccionado contiene hojas puras
                # Remueve las instancias del dataset que se contengan en la hoja

            # Si el atributo no contiene mas hojas impuras
                # Remueve el atributo del dataset

            break
