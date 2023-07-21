import copy
import random
from typing import List

from ..knapsack_problem.item import Item
from ..knapsack_problem.knapsack import Mochila


def linear_reduction(temperature, alpha):
    return temperature - alpha


def geometric_reduction(temperature, alpha):
    return temperature * (1 - alpha)


def gerar_itens_aleatorios(numero_itens: int,
                           valor_minimo: float,
                           valor_maximo: float,
                           peso_minimo: float,
                           peso_maximo: float,
                           tipo=int) -> List[Item]:
    itens = []
    for i in range(numero_itens):
        if tipo == "int":
            valor = random.randint(valor_minimo, valor_maximo)
            peso = random.randint(peso_minimo, peso_maximo)
        elif tipo == "float":
            valor = random.uniform(valor_minimo, valor_maximo)
            peso = random.uniform(peso_minimo, peso_maximo)
        item = Item(i, valor, peso)
        itens.append(item)
    return itens


def avaliar_mochila(mochila: Mochila) -> float:
    return sum([item.valor for item in mochila.itens])


def gerar_mochila_aleatoria(capacidade: int, itens: List[Item]) -> Mochila:
    mochila = Mochila(capacidade)
    n = random.randint(0, len(itens))
    for _ in range(n):
        item = random.choice(itens)
        mochila.adicionar_item(item)
    return mochila


def gerar_mochila_vizinha(mochila: Mochila, itens: List[Item]) -> Mochila:
    mochila_vizinha = Mochila(mochila.capacidade)
    mochila_vizinha.itens = copy.copy(mochila.itens)
    escolhas = ["adicionar_um_item", "retirar_e_adicionar_um_item"]
    decisao = random.choice(escolhas)
    if decisao == "adicionar_um_item":
        item = random.choice(itens)
        if not mochila_vizinha.adicionar_item(item):
            return gerar_mochila_vizinha(mochila, itens)
    elif decisao == "retirar_e_adicionar_um_item":
        if len(mochila_vizinha.itens) > 0:
            item = random.choice(mochila_vizinha.itens)
            mochila_vizinha.remover_item(item)
        item = random.choice(itens)
        mochila_vizinha.adicionar_item(item)
    return mochila_vizinha


def diferenca_mochilas(mochila_a: Mochila, mochila_b: Mochila) -> float:
    return avaliar_mochila(mochila_a) - avaliar_mochila(mochila_b)