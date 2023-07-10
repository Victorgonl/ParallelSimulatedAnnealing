import random


class Item:
    def __init__(self, id, valor, peso):
        self.id = id
        self.valor = valor
        self.peso = peso

def gerar_itens_aleatórios(número_de_itens,
                           valor_mínimo, valor_máximo,
                           peso_mínimo, peso_máximo,
                           tipo=int):
    itens = []
    for i in range(número_de_itens):
        if tipo == "int":
            valor = random.randint(valor_mínimo, valor_máximo)
            peso = random.randint(peso_mínimo, peso_máximo)
        elif tipo == "float":
            valor = random.uniform(valor_mínimo, valor_máximo)
            peso = random.uniform(peso_mínimo, peso_máximo)
        item = Item(i, valor, peso)
        itens.append(item)
    return itens