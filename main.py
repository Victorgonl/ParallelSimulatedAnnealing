import json
import datetime
import os
from typing import Any, Dict, List
import cpuinfo

from src import (
    SimulatedAnnealing,
    Item,
    Mochila,
    avaliar_mochila,
    diferenca_mochilas,
    geometric_reduction,
    gerar_itens_aleatorios,
    gerar_mochila_aleatoria,
    gerar_mochila_vizinha
)


TO_SAVE = False
TO_SAVE_POPULATION = TO_SAVE
SHOW_PROGRESS_BAR = not TO_SAVE

DATE = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
DIRECTORY = f"./data/{DATE}/"


def registrar_populacao(parametros_populacao: Dict[str, Any], itens: List[Item]) -> None:
    itens_dict = {"id": [item.id for item in itens],
                "valor": [item.valor for item in itens],
                "peso": [item.peso for item in itens]}

    with open(f"{DIRECTORY}pop_param.json", "w") as outfile:
        json.dump(parametros_populacao, outfile, indent=4)

    if TO_SAVE_POPULATION:
        with open(f"{DIRECTORY}pop.json", "w") as outfile:
            json.dump(itens_dict, outfile, indent=4)


def registrar_solucao_inicial(mochila_inicial: Mochila) -> None:
    mochila_inicial_dict = {"capacidade": mochila_inicial.capacidade,
                            "itens": [item.id for item in mochila_inicial.itens]}
    
    with open(f"{DIRECTORY}init_solution.json", "w") as outfile:
        json.dump(mochila_inicial_dict, outfile, indent=4)


def registrar_cpu_info() -> None:
    # parâmetros da(s) máquina(s)
    cpu_info = cpuinfo.get_cpu_info()
    
    with open(f"{DIRECTORY}cpu_info.json", "w") as outfile:
        json.dump(cpu_info, outfile, indent=4)


def registrar_experimentacao(parametros_experimentacao: Dict[str, Any]) -> None:
    with open(f"{DIRECTORY}exp_params.json", "w") as outfile:
        json.dump(parametros_experimentacao, outfile, indent=4)


def registrar_algoritmos(parametros_algoritmos: Dict[str, Any]) -> None:
    with open(f"{DIRECTORY}algoritm_params.json", "w") as outfile:
        json.dump(parametros_algoritmos, outfile, indent=4)


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
                funcao_resfriamento=geometric_reduction,
                solucao_inicial=mochila_inicial,
                itens=itens,
            )

            solução, registro = simulated_annealing.executar_paralelo(
                mostrar_barra_progresso=SHOW_PROGRESS_BAR,
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

            if TO_SAVE:
                with open(f"{DIRECTORY}run-PSA{numero_processos}-{i}.json", "w") as outfile :
                    json.dump(registro_dict, outfile, indent=4)

            print()


if __name__ == "__main__":
    os.makedirs(DIRECTORY, exist_ok=True) if TO_SAVE else None

    print()
    print("Experimentação:", DATE)
    print()

    parametros_algoritmos = {"temperatura_inicial": 1,
                            "temperatura_final": 0.1,
                            "taxa_resfriamento": 0.01,
                            "numero_vizinhos_explorar": 1000,
                            "forma_selecao": "optimal"}
    
    parametros_experimentacao = {"numero_execucoes": 1,
                                    "processes_number": [1, 2, 4, 8, 16]}
    
    capacidade_mochilas = 1.0
    
    parametros_populacao = {"numero_itens": 100000,
                            "valor_minimo" :0.0,
                            "valor_maximo": 1.0,
                            "peso_minimo": 0.0,
                            "peso_maximo": 1.0,
                            "tipo": "float"}

    itens = gerar_itens_aleatorios(parametros_populacao["numero_itens"],
                                parametros_populacao["valor_minimo"],
                                parametros_populacao["valor_maximo"],
                                parametros_populacao["peso_minimo"],
                                parametros_populacao["peso_maximo"],
                                parametros_populacao["tipo"])
    
    mochila_inicial = gerar_mochila_aleatoria(capacidade=capacidade_mochilas, itens=itens)
    
    if TO_SAVE:
        registrar_populacao(parametros_populacao, itens)
        registrar_solucao_inicial(mochila_inicial)
        registrar_cpu_info()
        registrar_experimentacao(parametros_experimentacao)
        registrar_algoritmos(parametros_algoritmos)

    executar_algoritmo_paralelo(parametros_experimentacao, parametros_algoritmos, mochila_inicial, itens)