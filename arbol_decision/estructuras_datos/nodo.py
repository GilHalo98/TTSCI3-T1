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
        nombre_atributo: str,
        conexiones: dict,
        *args,
        **kargs
    ) -> None:
        # ID del nodo en cuestion.
        self.id = id

        # Nombre del atributo que le pertenece el nodo.
        self.nombre_atributo = nombre_atributo

        # Diccionario de conexiones del nodo, con id del nodo de
        # conexion y los valores del atributo.
        self.conexiones = conexiones

        # Propiedades extra del nodo, propiedades no necesarias para
        # operaciones relacionadas al nodo o al grafo.
        self.propiedades = kargs

    def __str__(self) -> str:
        # Representacion del nodo en formato String.
        representacion_conexiones = ''

        return representacion_conexiones
