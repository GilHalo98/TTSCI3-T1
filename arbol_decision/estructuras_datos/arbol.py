'''
    Mantiene la estructura de datos de un Grafo, asi como algunas
    propiedades bases de estos.
'''


# Librerias propias.
from typing import Generator
from .nodo import Nodo


class Arbol(dict):
    '''
        La clase nodo es una representacion de una topologia de un arbol
        heredada de la clase diccionario, es posible agregar, eliminar,
        modificar, buscar, generar un grafico de la topologia del arbol,
        etc.

        La estructura de un arbol esta dada por un diccionario:

        arbol {
            id_nodo: Objeto_Nodo,
            ...
        }

        El id del nodo esta dado por una indexacion automatica de la
        misma clase.
    '''

    # Constructor de clase grafo.
    def __init__(self) -> None:
        # Se inicializa la clase padre.
        super().__init__()

        # Raiz del arbol.
        self.raiz = None

        # Generador de index del arbol.
        self.get_index = self.__get_index()

    def __str__(self) -> str:
        '''
            Genera  una representacion en string de la topologia
            del arbol.
        '''

        representacion = ''

        for id_nodo in self:

            if id_nodo is self.raiz:
                representacion += 'Raiz '

            representacion += '{}\n'.format(self[id_nodo])

        return representacion

    def __get_index(self) -> 'Generator[int, None, None]':
        # Indexacion de los nodos en el arbol.
        index = 0

        while True:
            yield index

            index += 1

    def esta_vacio(self) -> bool:
        # Retorna si existen nodos en el arbol.
        return True if len(self) <= 0 else False

    def inicializado(self) -> bool:
        # Retorna si el arbol se encuentra inicializado, si existe un
        # nodo raiz.
        return True if self.raiz is not None else False

    def agregar_conexion(
        self,
        id_nodo_a: 'str | int',
        id_nodo_b: 'str | int',
        costo: float = 1
    ) -> None:
        '''
            Agrega una conexion de un nodo A a un nodo B: A -> B.
        '''
        self[id_nodo_a].conectar_con(id_nodo_b, costo)

    def inicializar_nodo(
        self,
        id_nodo: 'str | int',
        conexiones: dict = {},
        *args,
        **kargs
    ) -> None:
        '''
            Inicializa un nodo en el arbol, la inicializacion de un nodo
            unicamente reserva el espacio en el arbol, asi como el id
            del nodo.
        '''
        self[id_nodo] = Nodo(
            id_nodo,
            conexiones,
            *args,
            **kargs
        )