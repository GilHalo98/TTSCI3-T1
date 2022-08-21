from math import log
from fractions import Fraction


def I(P: 'float | Fraction', base: 'int') -> float:
    return -log(P, base) if P != 0 else 0


def H(P: 'float | Fraction', I: 'float | Fraction') -> float:
    return P * I


def probabilidades(data):
    probabilidades = {}
    total = sum(list(data.values()))

    for dato in data:
        probabilidades[dato] = Fraction(data[dato], total)

    return probabilidades
