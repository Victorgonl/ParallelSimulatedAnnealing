import math
import tqdm
import random
import time
import threading


def parallel_simulated_annealing(temperatura_inicial,
                                 temperatura_final,
                                 taxa_de_resfriamento,
                                 gerar_solução_vizinha,
                                 comparar_soluções,
                                 avaliar_solução,
                                 função_de_resfriamento,
                                 itens,
                                 solução_inicial=None,
                                 número_de_vizinhos_a_explorar=1,
                                 número_de_threads=1):

    t = time.time()

    # registro
    registro = {"avaliação": [],
                "temperatura": [],
                "solução": [],
                "número_vizinhos_explorados": 0}

    # inicialização
    global temperatura_atual
    temperatura_atual = temperatura_inicial
    global solução_atual
    solução_atual = solução_inicial
    iteração = 0
    número_de_vizinhos_a_explorar_por_thread = [número_de_vizinhos_a_explorar // número_de_threads for _ in range(número_de_threads)]
    número_de_vizinhos_a_explorar_por_thread[-1] += número_de_vizinhos_a_explorar - sum(número_de_vizinhos_a_explorar_por_thread)

    # registrar avaliação e temperatura
    registro["avaliação"].append(avaliar_solução(solução_atual))
    registro["temperatura"].append(temperatura_atual)
    registro["solução"].append(solução_atual)

    # barra de progresso
    total = math.ceil(math.log(temperatura_final / temperatura_inicial, função_de_resfriamento(1, taxa_de_resfriamento)))
    barra_de_progresso = tqdm.tqdm(total=total, desc=f"Parallel Simulated Annealing - {número_de_threads} threads",
                                   bar_format="{l_bar}{bar}| {postfix}")

    # função para explorar vizinhos
    def explorar_vizinhos(soluções_vizinhas,
                          número_de_vizinhos_a_explorar):
        for _ in range(número_de_vizinhos_a_explorar):
            global solução_atual
            global temperatura_atual
            solução_vizinha = gerar_solução_vizinha(solução_atual, itens)
            erro = comparar_soluções(solução_atual, solução_vizinha)
            probabilidade = math.exp(-erro / temperatura_atual)
            soluções_vizinhas.append((solução_vizinha, erro, probabilidade))
            registro["número_vizinhos_explorados"] += 1

    # laço de temperatura
    while temperatura_atual > temperatura_final:
        # explorar vizinhos
        threads = []
        soluções_vizinhas = []

        for i in range(número_de_threads):
            thread = threading.Thread(target=explorar_vizinhos, args=(soluções_vizinhas, número_de_vizinhos_a_explorar_por_thread[i]))
            threads.append(thread)
            thread.start()

        # Aguardar até que todas as threads terminem
        for thread in threads:
            thread.join()

        # Selecionar a solução atual como a solução vizinha com o menor erro
        for (solução_vizinha, erro, probabilidade) in soluções_vizinhas:
            if erro < 0 or probabilidade > random.random():
                solução_atual = solução_vizinha

        # Chamar a função de resfriamento
        nova_temperatura = função_de_resfriamento(temperatura_atual, taxa_de_resfriamento)

        # Registrar avaliação e temperatura
        registro["avaliação"].append(avaliar_solução(solução_atual))
        registro["temperatura"].append(temperatura_atual)
        registro["solução"].append(solução_atual)

        # Atualizar a barra de progresso
        barra_de_progresso.set_postfix({"Temperatura": "{:.5f}".format(temperatura_atual),
                                        "Avaliação": "{:.5f}".format(registro["avaliação"][-1])})
        barra_de_progresso.update(1)
        barra_de_progresso.refresh()

        # Atualizar a temperatura
        temperatura_atual = nova_temperatura
        iteração += 1

    # Encerrar a barra de progresso
    barra_de_progresso.close()

    t = time.time() - t
    registro["run_time"] = t

    # Retorna a solução
    return solução_atual, registro