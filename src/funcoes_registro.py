import json
import cpuinfo
from typing import Any, Dict, List

from .mochila import Mochila
from .item import Item


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


def carregar_parametros_populacao(diretorio: str) -> Dict[str, Any]:
    with open(f"{diretorio}pop_param.json", "r") as infile:
        parametros_populacao = json.load(infile)
    return parametros_populacao


def carregar_populacao(diretorio: str) -> List[Item]:
    with open(f"{diretorio}pop.json", "r") as infile:
        itens_dict = json.load(infile)
    return [Item(id=item_id, valor=valor, peso=peso) for item_id, valor, peso in zip(itens_dict["id"], itens_dict["valor"], itens_dict["peso"])]


def registrar_solucao_inicial(mochila_inicial: Mochila, diretorio: str) -> None:
    mochila_inicial_dict = {"capacidade": mochila_inicial.capacidade,
                            "itens": [item.id for item in mochila_inicial.itens]}

    with open(f"{diretorio}init_solution.json", "w") as outfile:
        json.dump(mochila_inicial_dict, outfile, indent=4)


def carregar_solucao_inicial(diretorio: str, itens: Dict[str, Item]) -> Mochila:
    with open(f"{diretorio}init_solution.json", "r") as infile:
        mochila_dict = json.load(infile)
    mochila = Mochila(capacidade=mochila_dict["capacidade"])
    for item_id in mochila_dict["itens"]:
        for item in itens:
            if item.id == item_id:
                mochila.adicionar_item(item)
    return mochila


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