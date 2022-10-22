# Librerias de terceros.
import numpy as np
from progress.bar import Bar

# Librerias propias
from util.clases.cromosoma import Cromosoma
from util.algoritmos.search import descartar_pareja, eliminar_individuo


class Poblacion():

    def __init__(
        self,
        cantidad_poblacion,
        generaciones_max,
        poblacion_max,
        propiedades_poblacion
    ):
        # Conteo del id de los cromosomas.
        self.conteo_id = 0

        # propiedades de la problacion.
        self.propiedades_poblacion = propiedades_poblacion

        # Cantidad de pobladores inicial.
        self.cantidad_poblacion = cantidad_poblacion

        # Generaciones maximas.
        self.generaciones_max = generaciones_max

        # Poblacion maxima.
        self.poblacion_max = poblacion_max

        # Generacion en la que se encuentra la poblacion.
        self.generacion = 0

        # Aptitud global anterior, esto es usado en los criterios de
        # terminacion.
        self.aptitud_global_anterior = -1

        # Aptitud de la poblacion.
        self.aptitud_global = 0

        # Peso de la poblacion.
        self.peso_global = 0
        
        # Valor de la poblacion.
        self.valor_global = 0

        # Aptitud promedio de la poblacion.
        self.aptitud_promedio = 0

        # Lista de individuos en la poblacion.
        self.poblacion = self.__inicializar_poblacion()

        # Log de la poblacion.
        self.log = {}

        # Registramos la poblacion inicial.
        self.registrar_poblacion()

    # Regresa un string de la representacion de la poblacion.
    def __str__(self):
        representacion = 'Generacion {} aptitud global {} poblacion {}'.format(
            self.generacion,
            self.aptitud_global,
            self.cantidad_poblacion
        )

        return representacion

    # Calcula los parametros de la poblacion.
    def __calcular_parametros(self):
        # Cambiamos la generacion actual.
        self.generacion += 1

        # Se cuenta nuevamente la poblacion.
        self.cantidad_poblacion = len(self.poblacion)

        # Recalculamos la aptitud global y promedio.
        self.aptitud_global_anterior = self.aptitud_global
        self.aptitud_global = 0
        self.peso_global = 0
        self.valor_global = 0
        self.aptitud_promedio = 0

        for individuo in self.poblacion:
            self.aptitud_global += individuo.aptitud
            self.peso_global += individuo.peso_total
            self.valor_global += individuo.valor_total

        self.aptitud_promedio = round(
            self.aptitud_global / self.cantidad_poblacion,
            3
        )

        # Realizamos un registro de la poblacion.
        self.registrar_poblacion()

    # Inicializa la poblacion.
    def __inicializar_poblacion(self):
        poblacion = []
        self.aptitud_global = 0
        self.peso_global = 0
        self.valor_global = 0
        self.aptitud_promedio = 0

        # Generamos la poblacion inicial.
        for _ in range(self.cantidad_poblacion):
            cromosoma = Cromosoma(self.conteo_id, *self.propiedades_poblacion)
            self.aptitud_global += cromosoma.aptitud
            self.peso_global += cromosoma.peso_total
            self.valor_global += cromosoma.valor_total
            poblacion.append(cromosoma)
            self.conteo_id += 1

        # Calculamos la aptitud promedio.
        self.aptitud_promedio = round(
            self.aptitud_global / self.cantidad_poblacion,
            3
        )

        return poblacion

    # Se calcula la condicion de terminacion.
    def __condicion_terminacion(self):
        # Normalmente se usan dos criterios: correr el AG un número 
        # máximo de iteraciones (generaciones) o detenerlo cuando no
        # haya cambios en la población. Un tercer criterio es agregado
        # si en la poblacion solo existe un individuo, entonces el
        # algoritmo es terminado.

        criterio_1 = (self.generacion + 1) < self.generaciones_max
        criterio_2 = self.aptitud_global != self.aptitud_global_anterior
        criterio_3 = self.cantidad_poblacion > 1

        mensaje = '\n---> Algoritmo terminado'
        if (not criterio_1):
            mensaje += ' Generaciones maximas alcanzadas'

        if (not criterio_2):
            mensaje += ' Convergencia de solucion detectada'

        if (not criterio_3):
            mensaje += ' Poblacion insuficiente'

        if not (criterio_1 and criterio_2 and criterio_3):
            print(mensaje)

        return criterio_1 and criterio_2 and criterio_3

    # Registra el log de la poblacion.
    def registro(self):
        registro = ''
        propiedades = list(self.log[0].keys())

        for generacion in self.log:
            registro += 'Generacion {}'.format(generacion)

            for propiedad in propiedades[:-1]:
                registro += '\n\t {}: {}'.format(
                    propiedad,
                    self.log[generacion][propiedad]
                )

            registro += '\n\t {}:'.format(propiedades[-1])
            for individuo in self.log[generacion][propiedades[-1]]:
                for propiedad in individuo:
                    registro += '\n\t\t {}: {}'.format(
                        propiedad,
                        individuo[propiedad]
                    )
                registro += '\n'

        return registro

    # Registra en el log la poblacion actual.
    def registrar_poblacion(self):
        self.log[self.generacion] = {
            'aptitud global': self.aptitud_global,
            'peso global':  self.peso_global,
            'valor global': self.valor_global,
            'aptitud promedio': self.aptitud_promedio,
            'total de individuos': self.cantidad_poblacion,

            # Esta propiedad siempre tiene que ser la ultima.
            'poblacion': [{
                'id': individuo.id,
                'genes': str(individuo),
                'peso total': individuo.peso_total,
                'valor total': individuo.valor_total,
                'aptitud': individuo.aptitud,
            } for individuo in self.poblacion]
        }

    # Selecciona una pareja por medio de la ruleta de una lista auxiliar
    # de la poblacion, debido a que las parejas seleccionadas
    # se eliminaran de la lista auxiliar.
    def seleccionar_pareja(self, candidatos, limite_descare=0):
        # Se calcula la aptitud del grupo de candidatos, esto debido a
        # que las probabilidades de reproduccion son relativas al grupo.
        aptitud_grupo = 0

        # Lista de candidatos no aptos.
        candidatos_no_aptos = []

        for candidato in candidatos:
            if candidato.aptitud > limite_descare:
                aptitud_grupo += candidato.aptitud

            else:
                # Si la aptitud del individuo es de 0, entonces se
                # agrega a una lista de candidatos no aptos.
                candidatos_no_aptos.append(candidato)

        # Los candidatos no aptos se eliminan del grupo.
        for candidato_no_apto in candidatos_no_aptos:
            eliminar_individuo(candidato_no_apto, candidatos)

        # Realizamos el calculo de las probabilidades de reproduccion.
        probabilidades = [
            individuo.aptitud / aptitud_grupo for individuo in candidatos
        ]

        # Seleccionamos la pareja dependiendo de su
        # probabilidad de reproduccion.
        pareja = np.random.choice(
            candidatos,
            size=2,
            replace=False,
            p=probabilidades
        )

        # Descartamos la pareja ya seleccionada de la lista de candidatos.
        descartar_pareja(pareja, candidatos)

        return pareja

    # Proceso de seleccion del algoritmo genetico, retorna las parejas
    # generadas.
    def seleccion(self):
        parejas = []
        candidatos = self.poblacion.copy()

        while len(candidatos) > 1:
            pareja = self.seleccionar_pareja(candidatos)
            parejas.append(pareja)

        return parejas

    # Proceso de cruze de las parejas generadas, retorna
    # los hijos de estas.
    def cruze(self, parejas):
        nueva_poblacion = []
        for pareja in parejas:
            hijo_a, hijo_b = pareja[0] + pareja[1]

            hijo_a.id = self.conteo_id
            self.conteo_id += 1

            hijo_b.id = self.conteo_id
            self.conteo_id += 1

            nueva_poblacion.append(hijo_a)
            nueva_poblacion.append(hijo_b)

        return nueva_poblacion

    # Se selecciona la nueva poblacion de la siguiente generacion, esta
    # operacion se hace en base a un parametro, en este caso aquellos
    # que superen el promedio de aptitud seran seleccionados.
    def seleccionar_nueva_poblacion(self, hijos):
        candidatos = hijos + self.poblacion
        nueva_poblacion = []

        for candidato in candidatos:
            if candidato.aptitud >= self.aptitud_promedio:
                nueva_poblacion.append(candidato)

        # Si existe un limite en la poblacion.
        if self.poblacion_max > 0:
        # Verificamos si la poblacion no excede el limite.
            if len(nueva_poblacion) > self.poblacion_max:
                # Este corte de la poblacion se puede hacer con algun
                # metodo de muestreo.
                nueva_poblacion = nueva_poblacion[:self.poblacion_max - 1]

        return nueva_poblacion

    # Ejecuta el algoritmo genetico.
    def run(self):
        sufijo = '%(percent)d%%'
        mensaje = 'Procesando'
        maximo = self.generaciones_max - 1

        with Bar(mensaje, max=maximo, suffix=sufijo) as bar:
            while(self.__condicion_terminacion()):
                parejas = self.seleccion()
                hijos = self.cruze(parejas)
                nueva_poblacion = self.seleccionar_nueva_poblacion(hijos)
                self.poblacion = nueva_poblacion

                if len(self.poblacion) <= 1:
                    print('\n---> Algoritmo terminado, poblacion insuficiente')
                    break

                self.__calcular_parametros()

                bar.next()