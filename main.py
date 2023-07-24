import datetime
import json
import os
from typing import Any, Dict, List

from src import (
    SimulatedAnnealing,
    Item,
    Mochila,

    avaliar_mochila,
    diferenca_mochilas,
    reducao_geometrica,

    gerar_mochila_vizinha,

    registrar_algoritmos,
    registrar_cpu_info,
    registrar_experimentacao,
    registrar_populacao,
    registrar_solucao_inicial,

    carregar_parametros_populacao,
    carregar_populacao,
    carregar_solucao_inicial
)


# Variáveis globais
REGISTRAR = True
REGISTRAR_POPULACAO = True
MOSTRAR_BARRA_PROGRESSO = REGISTRAR

DATA = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
DIRETORIO = f"./data/{DATA}/"


def executar_algoritmo_paralelo(parametros_experimentacao: Dict[str, Any],
                                parametros_algoritmos: Dict[str, Any],
                                mochila_inicial: Mochila,
                                itens: List[Item]) -> None:
    k = 0

    for k in range(len(parametros_experimentacao["processes_number"])):

        for i in range(parametros_experimentacao["numero_execucoes"]):

            numero_processos = parametros_experimentacao["processes_number"][k]

            print(f"PSA{numero_processos}-{i}")

            simulated_annealing = SimulatedAnnealing(
                temperatura_inicial=parametros_algoritmos["temperatura_inicial"],
                temperatura_final=parametros_algoritmos["temperatura_final"],
                taxa_resfriamento=parametros_algoritmos["taxa_resfriamento"],
                numero_vizinhos_explorar=parametros_algoritmos["numero_vizinhos_explorar"],
                gerar_solucao_vizinha=gerar_mochila_vizinha,
                comparar_solucoes=diferenca_mochilas,
                avaliar_solucao=avaliar_mochila,
                funcao_resfriamento=reducao_geometrica,
                solucao_inicial=mochila_inicial,
                itens=itens,
            )

            solução, registro = simulated_annealing.executar_paralelo(
                mostrar_barra_progresso=MOSTRAR_BARRA_PROGRESSO,
                forma_selecao=parametros_algoritmos["forma_selecao"],
                numero_processos=numero_processos,
            )

            print("Tempo de execução: %s seconds" % registro["run_time"])
            print("Total de itens na mochila:", len(solução.itens))
            #print("Itens na mochila:", [item.id for item in solução.itens])
            print("Valor total na mochila:", avaliar_mochila(solução))
            print("Peso total na mochila:", solução.peso())
            print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

            registro_dict = {"execution_time": registro["run_time"],
                            "processes_number": numero_processos,
                            "value": registro["avaliação"],
                            "temperature": registro["temperatura"],
                            "exploited_neighbors": registro["número_vizinhos_explorados"],
                            "itens": [item.id for item in solução.itens],
                            "solution": [[item.id for item in solução.itens] for solução in registro["solução"]]}

            if REGISTRAR:
                with open(f"{DIRETORIO}run-PSA{numero_processos}-{i}.json", "w") as outfile :
                    json.dump(registro_dict, outfile, indent=4)

            print()


if __name__ == "__main__":
    """
    TODO:
    - Criar Notebook para mostrar métricas;
    - numero_vizinhos_explorar: 100, 1000, 10000;
    - Executar em laptop Victor e no PC Zanella;
    - Mudar nome dos logs de data.
    """

    os.makedirs(DIRETORIO, exist_ok=True) if REGISTRAR else None

    print()
    print("Experimentação:", DATA)
    print()

    parametros_algoritmos = {"temperatura_inicial": 1,
                            "temperatura_final": 0.1,
                            "taxa_resfriamento": 0.01,
                            "numero_vizinhos_explorar": 10000,
                            "forma_selecao": "optimal"}

    parametros_experimentacao = {"numero_execucoes": 10,
                                    "processes_number": [1, 2, 4, 8, 16]}

    parametros_populacao = carregar_populacao

    parametros_populacao = carregar_parametros_populacao("./parametros_iniciais/")

    itens = itens = carregar_populacao("./parametros_iniciais/")

    mochila_inicial = carregar_solucao_inicial("./parametros_iniciais/", itens)

    if REGISTRAR:
        registrar_populacao(parametros_populacao, itens, DIRETORIO, REGISTRAR_POPULACAO)
        registrar_solucao_inicial(mochila_inicial, DIRETORIO)
        registrar_cpu_info(DIRETORIO)
        registrar_experimentacao(parametros_experimentacao, DIRETORIO)
        registrar_algoritmos(parametros_algoritmos, DIRETORIO)

    executar_algoritmo_paralelo(parametros_experimentacao, parametros_algoritmos, mochila_inicial, itens)
