import json
import datetime
import os
import cpuinfo

from src.functions.helper_functions import avaliar_mochila, diferenca_mochilas, geometric_reduction, gerar_itens_aleatorios, gerar_mochila_aleatoria, gerar_mochila_vizinha
from src.simulated_annealing.simulated_annealing import SimulatedAnnealing


to_save = False
to_save_population = to_save
show_progress_bar = not to_save

date = datetime.datetime.now().strftime("%Y%m%d-%H%M")
directory = f"./data/{date}/"
os.makedirs(directory, exist_ok=True) if to_save else None

print()
print("Experimentação:", date)
print()


# ============================== POPULAÇÃO ============================== #

# parâmetros da população
parametros_populacao = {"número_de_itens": 100000,
                            "valor_mínimo" :0.0,
                            "valor_máximo": 1.0,
                            "peso_mínimo": 0.0,
                            "peso_máximo": 1.0,
                            "tipo": "float"}

# geração da população
itens = gerar_itens_aleatorios(parametros_populacao["número_de_itens"],
                               parametros_populacao["valor_mínimo"],
                               parametros_populacao["valor_máximo"],
                               parametros_populacao["peso_mínimo"],
                               parametros_populacao["peso_máximo"],
                               parametros_populacao["tipo"])

itens_dict = {"id": [item.id for item in itens],
              "valor": [item.valor for item in itens],
              "peso": [item.peso for item in itens]}

if to_save:
    with open(f"{directory}pop_param.json", "w") as outfile:
        json.dump(parametros_populacao, outfile, indent=4)

if to_save and to_save_population:
    with open(f"{directory}pop.json", "w") as outfile:
        json.dump(itens_dict, outfile, indent=4)


# ============================== SOLUÇÃO INICIAL ============================== #


# parâmetros da solução
capacidade_mochilas = 1.0

# geração da solução inicial
mochila_inicial = gerar_mochila_aleatoria(capacidade=capacidade_mochilas,
                                          itens=itens)

mochila_inicial_dict = {"capacidade": mochila_inicial.capacidade,
                        "itens": [item.id for item in mochila_inicial.itens]}

if to_save:
    with open(f"{directory}init_solution.json", "w") as outfile:
        json.dump(mochila_inicial_dict, outfile, indent=4)


# ============================== MÁQUINA ============================== #

# parâmetros da experimentação
parametros_experimentacao = {"número_de_execuções": 1,
                                "processes_number": [1, 2, 4, 8, 16]}

# parâmetros da(s) máquina(s)
cpu_info = cpuinfo.get_cpu_info()

if to_save:
    with open(f"{directory}exp_params.json", "w") as outfile:
        json.dump(parametros_experimentacao, outfile, indent=4)

    with open(f"{directory}cpu_info.json", "w") as outfile:
        json.dump(cpu_info, outfile, indent=4)


# ============================== ALGORITMOS ============================== #

# parâmetros do algoritmo
parametros_algoritmos = {"temperatura_inicial": 1,
                           "temperatura_final": 0.1,
                           "taxa_de_resfriamento": 0.01,
                           "número_de_vizinhos_a_explorar": 1000,
                           "forma_de_seleção": "optimal"}

if to_save:
    with open(f"{directory}algoritm_params.json", "w") as outfile:
        json.dump(parametros_algoritmos, outfile, indent=4)

""" # execução do algoritmo sequencial
for i in range(parametros_experimentacao["número_de_execuções"]):

    print(f"SSA-{i}")

    solução, registro = simulated_annealing(
        temperatura_inicial=parametros_algoritmos["temperatura_inicial"],
        temperatura_final=parametros_algoritmos["temperatura_final"],
        taxa_de_resfriamento=parametros_algoritmos["taxa_de_resfriamento"],
        número_de_vizinhos_a_explorar=parametros_algoritmos["número_de_vizinhos_a_explorar"],
        gerar_solução_vizinha=gerar_mochila_vizinha,
        comparar_soluções=diferença_entre_mochilas,
        avaliar_solução=avaliar_mochila,
        função_de_resfriamento=geometric_reduction,
        solução_inicial=mochila_inicial,
        itens=itens
    )

    print("Tempo de execução: %s seconds" % registro["run_time"])
    print("Total de itens na mochila:", len(solução.itens))
    print("Itens na mochila:", [item.id for item in solução.itens])
    print("Valor total na mochila:", avaliar_mochila(solução))
    print("Peso total na mochila:", solução.peso())
    print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

    registro_dict = {"execution_time": registro["run_time"],
                     "value": registro["avaliação"],
                     "temperature": registro["temperatura"],
                     "exploited_neighbors": registro["número_vizinhos_explorados"],
                     "itens": [item.id for item in solução.itens],
                     "solution": [[item.id for item in solução.itens] for solução in registro["solução"]]}

    with open(f"{directory}run-SSA-{i}.json", "w") as outfile:
        json.dump(registro_dict, outfile, indent=4)

    print() """

# execução do algoritmo paralelo
k = 0

for k in range(len(parametros_experimentacao["processes_number"])):

    for i in range(parametros_experimentacao["número_de_execuções"]):

        numero_processos = parametros_experimentacao["processes_number"][k]

        print(f"PSA{numero_processos}-{i}")

        simulated_annealing = SimulatedAnnealing(
            temperatura_inicial=parametros_algoritmos["temperatura_inicial"],
            temperatura_final=parametros_algoritmos["temperatura_final"],
            taxa_resfriamento=parametros_algoritmos["taxa_de_resfriamento"],
            numero_vizinhos_explorar=parametros_algoritmos["número_de_vizinhos_a_explorar"],
            gerar_solucao_vizinha=gerar_mochila_vizinha,
            comparar_solucoes=diferenca_mochilas,
            avaliar_solucao=avaliar_mochila,
            funcao_resfriamento=geometric_reduction,
            solucao_inicial=mochila_inicial,
            itens=itens,
        )

        solução, registro = simulated_annealing.executar_paralelo(
            mostrar_barra_progresso=show_progress_bar,
            forma_selecao=parametros_algoritmos["forma_de_seleção"],
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

        if to_save:
            with open(f"{directory}run-PSA{numero_processos}-{i}.json", "w") as outfile :
                json.dump(registro_dict, outfile, indent=4)

        print()