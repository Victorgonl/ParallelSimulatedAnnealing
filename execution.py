from src.functions.plot_functions import plotar_gráfico, plotar_gráfico_de_dispersão, plotar_itens
from src.knapsack_problem.item import gerar_itens_aleatórios
from src.knapsack_problem.knapsack import avaliar_mochila, diferença_entre_mochilas, gerar_mochila_aleatória, gerar_mochila_vizinha
from src.simulated_annealing.parallel_simulated_annealing import parallel_simulated_annealing
from src.simulated_annealing.reduction_functions import geometric_reduction
from src.simulated_annealing.simulated_annealing import simulated_annealing

import json
import datetime
import os
import cpuinfo


date = datetime.datetime.now().strftime("%Y%m%d-%H%M")
directory = f"./data/{date}/"
os.makedirs(directory, exist_ok=True)

print()
print("Experimentação:", date)
print()


# ============================== POPULAÇÃO ============================== #

# parâmetros da população
parâmetros_da_população = {"número_de_itens": 1000000,
                            "valor_mínimo" :0.0,
                            "valor_máximo": 1.0,
                            "peso_mínimo": 0.0,
                            "peso_máximo": 1.0,
                            "tipo": "float"}

# geração da população
itens = gerar_itens_aleatórios(parâmetros_da_população["número_de_itens"],
                               parâmetros_da_população["valor_mínimo"],
                               parâmetros_da_população["valor_máximo"],
                               parâmetros_da_população["peso_mínimo"],
                               parâmetros_da_população["peso_máximo"],
                               parâmetros_da_população["tipo"])

itens_dict = {"id": [item.id for item in itens],
              "valor": [item.valor for item in itens],
              "peso": [item.peso for item in itens]}

with open(f"{directory}pop_param.json", "w") as outfile:
    json.dump(parâmetros_da_população, outfile, indent=4)

with open(f"{directory}pop.json", "w") as outfile:
    json.dump(itens_dict, outfile, indent=4)



# ============================== SOLUÇÃO INICIAL ============================== #


# parâmetros da solução
capacidade_das_mochilas = 1.0

# geração da solução inicial
mochila_inicial = gerar_mochila_aleatória(capacidade=capacidade_das_mochilas,
                                          itens=itens)

mochila_inicial_dict = {"capacidade": mochila_inicial.capacidade,
                        "itens": [item.id for item in mochila_inicial.itens]}

with open(f"{directory}init_solution.json", "w") as outfile:
    json.dump(mochila_inicial_dict, outfile, indent=4)


# ============================== MÁQUINA ============================== #

# parâmetros da experimentação
parâmetros_da_experimentação = {"número_de_execuções": 100,
                                "processes_number": [1, 2, 4, 8, 16]}

with open(f"{directory}exp_params.json", "w") as outfile:
    json.dump(parâmetros_da_experimentação, outfile, indent=4)

# parâmetros da(s) máquina(s)
cpu_info = cpuinfo.get_cpu_info()

with open(f"{directory}cpu_info.json", "w") as outfile:
    json.dump(cpu_info, outfile, indent=4)


# ============================== ALGORITMOS ============================== #

# parâmetros do algoritmo
parâmetros_do_algoritmo = {"temperatura_inicial": 1,
                           "temperatura_final": 0.1,
                           "taxa_de_resfriamento": 0.01,
                           "número_de_vizinhos_a_explorar": 1000}

with open(f"{directory}algoritm_params.json", "w") as outfile:
    json.dump(parâmetros_do_algoritmo, outfile, indent=4)

""" # execução do algoritmo sequencial
for i in range(parâmetros_da_experimentação["número_de_execuções"]):

    print(f"SSA-{i}")

    solução, registro = simulated_annealing(
        temperatura_inicial=parâmetros_do_algoritmo["temperatura_inicial"],
        temperatura_final=parâmetros_do_algoritmo["temperatura_final"],
        taxa_de_resfriamento=parâmetros_do_algoritmo["taxa_de_resfriamento"],
        número_de_vizinhos_a_explorar=parâmetros_do_algoritmo["número_de_vizinhos_a_explorar"],
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

for k in range(len(parâmetros_da_experimentação["processes_number"])):

    for i in range(parâmetros_da_experimentação["número_de_execuções"]):

        número_de_processos = parâmetros_da_experimentação["processes_number"][k]

        print(f"PSA{número_de_processos}-{i}")

        solução, registro = parallel_simulated_annealing(
            temperatura_inicial=parâmetros_do_algoritmo["temperatura_inicial"],
            temperatura_final=parâmetros_do_algoritmo["temperatura_final"],
            taxa_de_resfriamento=parâmetros_do_algoritmo["taxa_de_resfriamento"],
            número_de_vizinhos_a_explorar=parâmetros_do_algoritmo["número_de_vizinhos_a_explorar"],
            gerar_solução_vizinha=gerar_mochila_vizinha,
            comparar_soluções=diferença_entre_mochilas,
            avaliar_solução=avaliar_mochila,
            função_de_resfriamento=geometric_reduction,
            solução_inicial=mochila_inicial,
            itens=itens,
            número_de_processos=número_de_processos
        )

        print("Tempo de execução: %s seconds" % registro["run_time"])
        print("Total de itens na mochila:", len(solução.itens))
        print("Itens na mochila:", [item.id for item in solução.itens])
        print("Valor total na mochila:", avaliar_mochila(solução))
        print("Peso total na mochila:", solução.peso())
        print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

        registro_dict = {"execution_time": registro["run_time"],
                        "processes_number": número_de_processos,
                        "value": registro["avaliação"],
                        "temperature": registro["temperatura"],
                        "exploited_neighbors": registro["número_vizinhos_explorados"],
                        "itens": [item.id for item in solução.itens],
                        "solution": [[item.id for item in solução.itens] for solução in registro["solução"]]}

        with open(f"{directory}run-PSA{número_de_processos}-{i}.json", "w") as outfile:
            json.dump(registro_dict, outfile, indent=4)

        print()