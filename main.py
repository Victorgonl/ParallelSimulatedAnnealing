from src.functions.plot_functions import plotar_gráfico, plotar_gráfico_de_dispersão, plotar_itens
from src.knapsack_problem.item import gerar_itens_aleatórios
from src.knapsack_problem.knapsack import avaliar_mochila, diferença_entre_mochilas, gerar_mochila_aleatória, gerar_mochila_vizinha
from src.simulated_annealing.parallel_simulated_annealing import parallel_simulated_annealing
from src.simulated_annealing.reduction_functions import geometric_reduction
from src.simulated_annealing.simulated_annealing import simulated_annealing

import time

# parâmetros da população
número_de_itens = 10000
valor_mínimo = 0.0
valor_máximo = 1.0
peso_mínimo = 0.0
peso_máximo = 1.0
tipo = float

# geração da população
itens = gerar_itens_aleatórios(número_de_itens=número_de_itens,
                               valor_mínimo=valor_mínimo,
                               valor_máximo=valor_máximo,
                               peso_mínimo=peso_mínimo,
                               peso_máximo=peso_máximo,
                               tipo=tipo,)

# parâmetros da solução
capacidade_das_mochilas = 1.0

# geração da solução inicial
mochila_inicial = gerar_mochila_aleatória(capacidade=capacidade_das_mochilas,
                                          itens=itens)

# parâmetros do algoritmo
temperatura_inicial = 100
temperatura_final = 0.1
taxa_de_resfriamento = 0.1
gerar_solução_vizinha = gerar_mochila_vizinha
comparar_soluções = diferença_entre_mochilas
avaliar_solução = avaliar_mochila
solução_inicial = mochila_inicial
temperature_reduction_function = geometric_reduction


# execução do algoritmo
t_1 = time.time()

solução, registro = simulated_annealing(
    temperatura_inicial,
    temperatura_final,
    taxa_de_resfriamento,
    gerar_solução_vizinha,
    comparar_soluções,
    avaliar_solução,
    temperature_reduction_function,
    solução_inicial=solução_inicial,
    itens=itens,
    número_de_vizinhos_explorados=4000
)

scatter_solução = {"x": [item.peso for item in solução.itens],
                   "y": [item.valor for item in solução.itens],
                   "s": 3,
                   "label": "Itens da solução",
                   "color": "orangered"}
title = "Itens selecionados na solução"
x_label = "peso"
y_label = "valor"

print("Total de itens na mochila:", len(solução.itens))
print("Itens na mochila:", [item.id for item in solução.itens])
print("Valor total na mochila:", avaliar_mochila(solução))
print("Peso total na mochila:", solução.peso())

print("--- %s seconds ---" % (time.time() - t_1))


# execução do algoritmo paralelo
t_2 = time.time()

solução, registro = parallel_simulated_annealing(
    temperatura_inicial,
    temperatura_final,
    taxa_de_resfriamento,
    gerar_solução_vizinha,
    comparar_soluções,
    avaliar_solução,
    temperature_reduction_function,
    solução_inicial=solução_inicial,
    itens=itens,
    número_de_vizinhos_explorados=1000,
    número_de_threads=4
)

scatter_solução = {"x": [item.peso for item in solução.itens],
                   "y": [item.valor for item in solução.itens],
                   "s": 3,
                   "label": "Itens da solução",
                   "color": "orangered"}
title = "Itens selecionados na solução"
x_label = "peso"
y_label = "valor"

print("Total de itens na mochila:", len(solução.itens))
print("Itens na mochila:", [item.id for item in solução.itens])
print("Valor total na mochila:", avaliar_mochila(solução))
print("Peso total na mochila:", solução.peso())

print("--- %s seconds ---" % (time.time() - t_2))