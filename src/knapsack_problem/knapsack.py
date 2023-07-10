import random
import copy


class Mochila:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.itens = []

    def adicionar_item(self, item):
        for item_na_mochila in self.itens:
            if item_na_mochila.id == item.id:
                return False
        if item.peso + self.peso() <= self.capacidade:
            self.itens.append(item)
            return True
        return False

    def remover_item(self, item):
        self.itens.remove(item)

    def peso(self):
        return sum([item.peso for item in self.itens])

def avaliar_mochila(mochila):
    return sum([item.valor for item in mochila.itens])

def gerar_mochila_aleatória(capacidade, itens) -> Mochila:
    mochila = Mochila(capacidade)
    n = random.randint(0, len(itens))
    for _ in range(n):
        item = random.choice(itens)
        mochila.adicionar_item(item)
    return mochila

def gerar_mochila_vizinha(mochila, itens):
    mochila_vizinha = Mochila(mochila.capacidade)
    mochila_vizinha.itens = copy.copy(mochila.itens)
    escolhas = ["adicionar_um_item", "retirar_e_adicionar_um_item"]
    decisão = random.choice(escolhas)
    if decisão == "adicionar_um_item":
        item = random.choice(itens)
        if not mochila_vizinha.adicionar_item(item):
            return gerar_mochila_vizinha(mochila, itens)
    elif decisão == "retirar_e_adicionar_um_item":
        if len(mochila_vizinha.itens) > 0:
            item = random.choice(mochila_vizinha.itens)
            mochila_vizinha.remover_item(item)
        item = random.choice(itens)
        mochila_vizinha.adicionar_item(item)
    return mochila_vizinha

def diferença_entre_mochilas(mochila_a, mochila_b):
    return avaliar_mochila(mochila_a) - avaliar_mochila(mochila_b)