class Nodo():
    '''
        Componente estructural del arbol, los nodos contienen la
        clausula, conexiones, id, valor, etc.

        Las conexiones estan formateadas de la siguiente forma

        conexiones {
            valor_atributo: id_conexion,
            ...
        }
    '''

    def __init__(
        self,
        id: int,
        conexiones: dict,
        *args,
        **kargs
    ) -> None:
        # ID del nodo en cuestion.
        self.id = id

        # Diccionario de conexiones del nodo, con id del nodo de
        # conexion y los costos de las conexiones.
        self.conexiones = conexiones

        # Propiedades extra del nodo, propiedades no necesarias para
        # operaciones relacionadas al nodo o al grafo.
        self.propiedades = kargs

    def __str__(self) -> str:
        '''
            Representacion del nodo y sus conexiones en string.

            Esta representacion deberia de hacerse recorriendo el arbol
            por medio de DFS.
        '''
        if self.es_hoja():
            representacion = 'Hoja {}'

        else:
            representacion = 'Nodo {}'

            lista_conexiones = list(self.conexiones.keys())

            representacion += ' -> '

            for id_conexion in lista_conexiones[:-1]:
                representacion += '{}: {}, '.format(
                    str(id_conexion),
                    self.conexiones[id_conexion]
                )

            representacion += '{}: {}'.format(
                    str(lista_conexiones[-1]),
                    self.conexiones[lista_conexiones[-1]]
                )


        return representacion.format(self.id)

    def es_hoja(self) -> bool:
        '''
            Retorna True si el numero de conexiones es mayor que 0,
            retorna false si este no es el caso.
        '''
        return False if len(self.conexiones) >= 1 else True

    def conectar_con(
        self,
        id_nodo: 'str | int',
        costo: float = 1
    ) -> None:
        '''
            Genera una conexion desde el nodo hasta un nodo dado.
        '''
        self.conexiones[id_nodo] = costo
