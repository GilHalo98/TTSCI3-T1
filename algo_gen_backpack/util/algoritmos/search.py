# Busca una pareja en la poblacion y la elimina de esta.
def descartar_pareja(pareja, lista_individuos):
    pareja_eliminada = []

    for individuo in pareja:
        pareja_eliminada.append(eliminar_individuo(individuo, lista_individuos))

    return pareja_eliminada

# Elimina un individuo de la poblacion.
def eliminar_individuo(individuo, lista_individuos):
    index = buscar_index_individuo(individuo, lista_individuos)
    return lista_individuos.pop(index)

# Busca el individuo dado su id en una poblacion.
def buscar_index_individuo(buscado, lista_individuos):
    index = 0

    for individuo in lista_individuos:

        if individuo.id == buscado.id:
            return index

        index += 1

    return None