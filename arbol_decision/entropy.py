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


def probabilidades(data):
    probabilidades = {}
    total = sum(list(data.values()))

    for dato in data:
        probabilidades[dato] = Fraction(data[dato], total)

    return probabilidades


def printPretty(P, I, H):
    print('Datos:')
    for pi, Ii, Hi in zip(P, I, H):
        msj = pi
        msj += ': P {0:.0f}%'.format(float(P[pi]*100))
        msj += ' I {0:.2f}'.format(Ii)
        msj += ' H {0:.2f}'.format(Hi)
        print('\t' + msj)
    print()
    print('H(E): {0:.2f}'.format(sum(H)))
    print('I(E): {0:.2f}'.format(sum(I)))
    

def main():
    datasets = [
        {'rojo': 5, 'azul': 1},
        {'rojo': 1, 'azul': 14},
        {'rojo': 4, 'azul': 4},
    ]
    base = 2

    for dataset in datasets:

        prob = probabilidades(dataset)

        P = list(prob.values())
        i = I(*P, base=base)
        h = H(*P, base=base)

        printPretty(prob, i, h)
        print('-'*50)


if __name__ == '__main__':
    system('clear')
    main()
