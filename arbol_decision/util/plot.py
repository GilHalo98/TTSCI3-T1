'''
    Funciones para graficar cosas.
'''

# Librerias de terceros.
import graphviz

# Librerias propias.
from modelos.arbol_decision import Arbol_Decision


def graficar_arbol_decision(
    modelo_decision: Arbol_Decision,
    archivo_salida: str,
) -> None:
    '''
        Genera un archivo de salida con la representacion grafica
        del modelo, este es generado a apartir de graphviz, se
        generan dos archivos, uno de tipo scv y otro de lenguaje
        DOT.
    '''

    # Inicializamos la clase graficador de graphviz.
    grafico = graphviz.Digraph(
        comment='Test',
        format='svg'
    )

    # Recuperamos la topologia del modelo.
    arbol = modelo_decision.get_arbol()

    for id_nodo in arbol:
        nodo = arbol[id_nodo]

        contenido = ''
        if nodo.es_hoja():
            contenido += 'Valor de {}: {}'.format(
                modelo_decision.atributo_meta,
                nodo.propiedades['valor_meta']
            )

        else:
            contenido += 'Atributo: {}'.format(nodo.propiedades['atributo'])
            contenido += '\nPureza: {0:.2f}'.format(
                nodo.propiedades['pureza']
            )

        contenido += '\nDatos en segmento: {}'.format(
            nodo.propiedades['cantidad_datos']
        )

        grafico.node(
            id_nodo,
            contenido,
            shape='rectangle',
            style='filled',
            color='0.58 {} 0.8'.format(nodo.propiedades['pureza'])
        )

        for id_conexion in nodo.conexiones:
            grafico.edge(
                id_nodo,
                id_conexion,
                str(nodo.conexiones[id_conexion])
            )

    # Establecemos que no se puedan sobreponer los nodos.
    grafico.attr(overlap='false', compound='true')

    # Por ultimo renderiza el grafo en un archivo svg.
    grafico.render(filename=archivo_salida)