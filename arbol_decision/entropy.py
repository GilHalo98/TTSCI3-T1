from math import log
from os import system
from fractions import Fraction


def I(*datos, base=10):
    inf_mutua = []

    for E in datos:
        inf_mutua.append(-log(E, base))

    return inf_mutua


def H(*datos, base=10):
    entropia = []

    inf_mutua = I(*datos, base=base)

    for E, Ie in zip(datos, inf_mutua):
        entropia.append(E * Ie)

    return entropia


def I(P, base):
    inf_mutua = []

    for Pi in P:
        inf_mutua.append(-log(Pi, base))

    return inf_mutua


def H(P, I):
    entropia = []

    for Pi, Ii in zip(P, I):
        entropia.append(Pi * Ii)

    return entropia


def probabilidades(data):
    probabilidades = {}
    total = sum(list(data.values()))

    for dato in data:
        probabilidades[dato] = Fraction(data[dato], total)

    return probabilidades
