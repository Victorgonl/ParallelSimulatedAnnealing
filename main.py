from src.functions.plot_functions import plotar_gráfico, plotar_gráfico_de_dispersão, plotar_itens
from src.knapsack_problem.item import gerar_itens_aleatórios
from src.knapsack_problem.knapsack import avaliar_mochila, diferença_entre_mochilas, gerar_mochila_aleatória, gerar_mochila_vizinha
from src.simulated_annealing.parallel_simulated_annealing import parallel_simulated_annealing
from src.simulated_annealing.reduction_functions import geometric_reduction
from src.simulated_annealing.simulated_annealing import simulated_annealing

import time

# parâmetros da população
número_de_itens = 100000
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
temperatura_inicial = 1
temperatura_final = 0.1
taxa_de_resfriamento = 0.01
gerar_solução_vizinha = gerar_mochila_vizinha
comparar_soluções = diferença_entre_mochilas
avaliar_solução = avaliar_mochila
solução_inicial = mochila_inicial
temperature_reduction_function = geometric_reduction
número_de_vizinhos_a_explorar = 1000


# execução do algoritmo sequencial
print("Sequential Simulated Annealing")
t = time.time()

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
    número_de_vizinhos_a_explorar=número_de_vizinhos_a_explorar
)

print("Total de itens na mochila:", len(solução.itens))
print("Itens na mochila:", [item.id for item in solução.itens])
print("Valor total na mochila:", avaliar_mochila(solução))
print("Peso total na mochila:", solução.peso())
print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

print("--- %s seconds ---" % (time.time() - t))

# execução do algoritmo paralelo (1 thread)
t = time.time()

número_de_threads = 1
print(f"Parallel Simulated Annealing ({número_de_threads} threads)")

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
    número_de_vizinhos_a_explorar=número_de_vizinhos_a_explorar,
    número_de_threads=número_de_threads
)

print("Total de itens na mochila:", len(solução.itens))
print("Itens na mochila:", [item.id for item in solução.itens])
print("Valor total na mochila:", avaliar_mochila(solução))
print("Peso total na mochila:", solução.peso())
print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

print("--- %s seconds ---" % (time.time() - t))


# execução do algoritmo paralelo (1 thread)
t = time.time()

número_de_threads = 2
print(f"Parallel Simulated Annealing ({número_de_threads} threads)")

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
    número_de_vizinhos_a_explorar=número_de_vizinhos_a_explorar * número_de_threads,
    número_de_threads=número_de_threads
)

print("Total de itens na mochila:", len(solução.itens))
print("Itens na mochila:", [item.id for item in solução.itens])
print("Valor total na mochila:", avaliar_mochila(solução))
print("Peso total na mochila:", solução.peso())
print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

print("--- %s seconds ---" % (time.time() - t))


# execução do algoritmo paralelo (1 thread)
t = time.time()

número_de_threads = 4
print(f"Parallel Simulated Annealing ({número_de_threads} threads)")

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
    número_de_vizinhos_a_explorar=número_de_vizinhos_a_explorar,
    número_de_threads=número_de_threads
)

print("Total de itens na mochila:", len(solução.itens))
print("Itens na mochila:", [item.id for item in solução.itens])
print("Valor total na mochila:", avaliar_mochila(solução))
print("Peso total na mochila:", solução.peso())
print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

print("--- %s seconds ---" % (time.time() - t))


# execução do algoritmo paralelo (1 thread)
t = time.time()

número_de_threads = 6
print(f"Parallel Simulated Annealing ({número_de_threads} threads)")

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
    número_de_vizinhos_a_explorar=número_de_vizinhos_a_explorar,
    número_de_threads=número_de_threads
)

print("Total de itens na mochila:", len(solução.itens))
print("Itens na mochila:", [item.id for item in solução.itens])
print("Valor total na mochila:", avaliar_mochila(solução))
print("Peso total na mochila:", solução.peso())
print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

print("--- %s seconds ---" % (time.time() - t))


# execução do algoritmo paralelo (1 thread)
t = time.time()

número_de_threads = 8
print(f"Parallel Simulated Annealing ({número_de_threads} threads)")

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
    número_de_vizinhos_a_explorar=número_de_vizinhos_a_explorar,
    número_de_threads=número_de_threads
)

print("Total de itens na mochila:", len(solução.itens))
print("Itens na mochila:", [item.id for item in solução.itens])
print("Valor total na mochila:", avaliar_mochila(solução))
print("Peso total na mochila:", solução.peso())
print("Número de vizinhos explorados:", registro["número_vizinhos_explorados"])

print("--- %s seconds ---" % (time.time() - t))