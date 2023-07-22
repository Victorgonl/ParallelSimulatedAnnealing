import copy
import random
import json
import cpuinfo
from typing import Any, Dict, List

from .item import Item
from .mochila import Mochila


def reducao_linear(temperature, alpha):
    return temperature - alpha


def reducao_geometrica(temperature, alpha):
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


def registrar_populacao(parametros_populacao: Dict[str, Any],
                        itens: List[Item],
                        diretorio: str,
                        registrar_populacao: bool) -> None:
    
    itens_dict = {"id": [item.id for item in itens],
                "valor": [item.valor for item in itens],
                "peso": [item.peso for item in itens]}

    with open(f"{diretorio}pop_param.json", "w") as outfile:
        json.dump(parametros_populacao, outfile, indent=4)

    if registrar_populacao:
        with open(f"{diretorio}pop.json", "w") as outfile:
            json.dump(itens_dict, outfile, indent=4)


def registrar_solucao_inicial(mochila_inicial: Mochila, diretorio: str) -> None:
    mochila_inicial_dict = {"capacidade": mochila_inicial.capacidade,
                            "itens": [item.id for item in mochila_inicial.itens]}
    
    with open(f"{diretorio}init_solution.json", "w") as outfile:
        json.dump(mochila_inicial_dict, outfile, indent=4)


def registrar_cpu_info(diretorio: str) -> None:
    # parâmetros da(s) máquina(s)
    cpu_info = cpuinfo.get_cpu_info()
    
    with open(f"{diretorio}cpu_info.json", "w") as outfile:
        json.dump(cpu_info, outfile, indent=4)


def registrar_experimentacao(parametros_experimentacao: Dict[str, Any], diretorio: str) -> None:
    with open(f"{diretorio}exp_params.json", "w") as outfile:
        json.dump(parametros_experimentacao, outfile, indent=4)


def registrar_algoritmos(parametros_algoritmos: Dict[str, Any], diretorio: str) -> None:
    with open(f"{diretorio}algoritm_params.json", "w") as outfile:
        json.dump(parametros_algoritmos, outfile, indent=4)
