# Importa librerias estandar.
from random import random, randint


class Cromosoma():

    def __init__(
        self,
        id,
        longitud,
        propiedades,
        peso_max,
        probabilidad_mutacion,
        genes=None,
        id_predecesor_a=None,
        id_predecesor_b=None
    ):
        # Id del cromosoma.
        self.id = id

        # Id de los padres.
        self.id_predecesor_a = id_predecesor_a
        self.id_predecesor_b = id_predecesor_b

        # Longitud del cormosoma, cantidad de genes.
        self.longitud = longitud

        # Propiedades del cromosoma.
        self.propiedades = propiedades

        # Variables a optimizar.
        self.peso_max = peso_max

        # Probabilidad de que algun gen mute.
        self.probabilidad_mutacion = probabilidad_mutacion

        # Asignamos un index de cruze, este index esta basado en el
        # cruze de recombinacion de un punto, que en este caso es el
        # punto medio del vector de genes.
        self.index_cruze = int(self.longitud / 2)

        # Peso total del cromosoma.
        self.peso_total = 0

        # Valor total del cromosoma.
        self.valor_total = 0

        # Aptitud del cromosoma.
        self.aptitud = 0

        # Si no se asigna un cromosoma se genera uno aleatorio.
        if genes is None:
            # Vector de genes, contiene una lista de 1 y 0, el 1 indica
            # que el gen esta activo.
            self.genes = self.__inicializar_genes()
        
        else:
            self.genes = genes
            self.__calcular_parametros()

    # Retorna un string de la representacion del cromosoma.
    def __str__(self):
        representacion = '<'

        for gen in self.genes[:-1]:
            representacion += str(gen) + ', '

        representacion += str(self.genes[-1]) + '>'

        return representacion

    # Realiza el cruze entre dos cromosomas, este metodo de cruze genera
    # dos cromosomas disntintos.
    def __add__(self, pareja):
        division_a = pareja.dividir_cromosoma()
        division_b = self.dividir_cromosoma()

        genes_a = division_a[0] + division_b[1]
        genes_b = division_b[0] + division_a[1]

        hijo_a = Cromosoma(
            0,
            self.longitud,
            self.propiedades,
            self.peso_max,
            self.probabilidad_mutacion,
            genes_a,
            self.id,
            pareja.id,
        )

        hijo_b = Cromosoma(
            0,
            self.longitud,
            self.propiedades,
            self.peso_max,
            self.probabilidad_mutacion,
            genes_b,
            self.id,
            pareja.id,
        )

        return hijo_a, hijo_b

    # Calcula los parametros del cromosoma.
    def __calcular_parametros(self):
        # Restablecemos el peso y valor total a 0.
        self.peso_total = 0
        self.valor_total = 0

        # Por cada gen en el cromosoma.
        for index in range(self.longitud):
            # Si el gen muta, se intercala el valor del gen.
            if random() <= self.probabilidad_mutacion:
                self.genes[index] = 1 if self.genes[index] else 0

            # Si el gen esta activo.
            if self.genes[index]:
                # Calculamos el peso y valor total.
                self.peso_total += self.propiedades['peso'][index]
                self.valor_total += self.propiedades['valor'][index]

        # Calculamos la aptitud, si el peso total excede el peso maximo
        # la aptitud automaticamente de establece a 0.
        if self.peso_total <= self.peso_max:
            self.aptitud = self.valor_total / self.peso_max

    # Genera un cromosoma aleatorio.
    def __inicializar_genes(self):
        # Generamos un template del cromosoma vacio.
        cromosoma = [0 for _ in range(self.longitud)]

        # Restablecemos el peso y valor total a 0.
        self.peso_total = 0
        self.valor_total = 0
        self.aptitud = 0

        # Por cada gen en el cromosoma.
        for index in range(self.longitud):
            # Selecciona aleatoriamente si el gen se activa o permanece
            # inactivo.
            gen = randint(0, 1)

            # Si el gen se activa y el peso total no excede el maximo.
            if gen and (self.peso_total < self.peso_max):
                peso = self.propiedades['peso'][index]
                valor = self.propiedades['valor'][index]

                # Si el peso a agregar y el peso total no
                # exceden el peso maximo.
                if (self.peso_total + peso) < self.peso_max:
                    self.peso_total += peso
                    self.valor_total += valor

                    cromosoma[index] = gen

            # Si por alguna razon el peso total es exactamente
            # al peso maximo.
            if self.peso_total == self.peso_max:
                break

        # Al crear el cromosoma de esta forma se emiten cromosomas con
        # aptitud 0, que sobrepasen el peso maximo, por esta razon
        # la aptitud de calcular como (valor total / peso total).
        self.aptitud = self.valor_total / self.peso_max

        return cromosoma

    # Divide los genes del cromosoma.
    def dividir_cromosoma(self):
        return self.genes[:self.index_cruze], self.genes[self.index_cruze:]