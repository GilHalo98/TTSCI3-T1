from csv import DictWriter
from os import system
from random import choice


def main():
    print('---| Generando instancia...')

    valores_esperados = {
        'Alt': [True, False],
        'Bar': [True, False],
        'Vier': [True, False],
        'Ham': [True, False],
        'Clientes': ['algunos', 'lleno', 'ninguno'],
        'Precio': ['caro', 'varato', 'razonable'],
        'Llov': [True, False],
        'Res': [True, False],
        'Tipo': ['Frances', 'Mexicana', 'China'],
        'Est': [10, 20, 60],
        'Esperar': [True, False]
    }

    instancias = []

    total_instancias = 10

    with open('instancia_prueba.csv', 'w+') as obj_csv:
        atributos = list(valores_esperados.keys())
        cabezal = DictWriter(obj_csv, fieldnames=atributos)
        cabezal.writeheader()

        while total_instancias > 0:
            instancia = {}

            for atr in valores_esperados:
                instancia[atr] = choice(valores_esperados[atr])

            instancias.append(instancia)
            cabezal.writerow(instancia)
            total_instancias -= 1


if __name__ == '__main__':
    system('clear')
    main()
