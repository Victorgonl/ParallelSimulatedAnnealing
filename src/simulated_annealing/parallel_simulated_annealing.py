import math
import tqdm
import random
import time
import multiprocessing


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
                                 número_de_processos=1):

    # inicializa a contagem de tempo
    t = time.time()

    # inicialização
    temperatura_atual = temperatura_inicial
    solução_atual = solução_inicial
    iteração = 0
    número_vizinhos_explorar_por_preocesso = [número_de_vizinhos_a_explorar // número_de_processos for _ in range(número_de_processos)]
    número_vizinhos_explorar_por_preocesso[-1] += número_de_vizinhos_a_explorar - sum(número_vizinhos_explorar_por_preocesso)

    # registro inicial das informações
    registro = {"avaliação": [],
                "temperatura": [],
                "solução": [],
                "número_vizinhos_explorados": 0}
    registro["avaliação"].append(avaliar_solução(solução_atual))
    registro["temperatura"].append(temperatura_atual)
    registro["solução"].append(solução_atual)

    # barra de progresso
    total = math.ceil(math.log(temperatura_final / temperatura_inicial, função_de_resfriamento(1, taxa_de_resfriamento)))
    barra_de_progresso = tqdm.tqdm(total=total, desc=f"Parallel Simulated Annealing - {número_de_processos} processes",
                                   bar_format="{l_bar}{bar}| {postfix}")

    # função para explorar vizinhos
    def explorar_vizinhos(lock,
                          process_id,
                          soluções_vizinhas,
                          número_vizinhos_explorar,
                          vizinhos_explorados):
        for _ in range(número_vizinhos_explorar):
            solução_vizinha = gerar_solução_vizinha(solução_atual, itens)
            erro = comparar_soluções(solução_atual, solução_vizinha)
            if erro < 0:
                    soluções_vizinhas.append(solução_vizinha)
            else:
                probabilidade = math.exp(-erro / temperatura_atual)
                x = random.random()
                if probabilidade > x:
                    soluções_vizinhas.append(solução_vizinha)
            vizinhos_explorados[process_id] += 1

    # laço de temperatura
    while temperatura_atual > temperatura_final:

        # explorar vizinhos
        soluções_vizinhas = multiprocessing.Manager().list()
        vizinhos_explorados = multiprocessing.Manager().list([0 for _ in range(número_de_processos)])

        # locker para processos
        lock = multiprocessing.Lock()

        # cria e inicia os processos
        processes = []
        for i in range(número_de_processos):
            process = multiprocessing.Process(target=explorar_vizinhos, args=(lock,
                                                                              i,
                                                                              soluções_vizinhas,
                                                                              número_vizinhos_explorar_por_preocesso[i],
                                                                              vizinhos_explorados))
            processes.append(process)
            process.start()

        # sincroniza os processos
        for process in processes:
            process.join()

        # encerra os processos
        for process in processes:
            process.close()

        '''
        # seleciona a solução atual como uma aleatória entre as vizinhas exploradas
        solução_atual = random.choice(soluções_vizinhas) if soluções_vizinhas else solução_atual
        '''

        # seleciona solução vizinha com base na temperatura
        for solução_vizinha in soluções_vizinhas:
            erro = comparar_soluções(solução_atual, solução_vizinha)
            if erro < 0:
                solução_atual = solução_vizinha
            else:
                probabilidade = math.exp(-erro / temperatura_atual)
                x = random.random()
                if probabilidade > x:
                    solução_atual = solução_vizinha

        # registra as informações
        registro["número_vizinhos_explorados"] += sum(vizinhos_explorados)
        registro["avaliação"].append(avaliar_solução(solução_atual))
        registro["temperatura"].append(temperatura_atual)
        registro["solução"].append(solução_atual)

        # atualiza a barra de progresso
        barra_de_progresso.set_postfix({"Temperatura": "{:.5f}".format(temperatura_atual),
                                        "Avaliação": "{:.5f}".format(registro["avaliação"][-1])})
        barra_de_progresso.update(1)
        barra_de_progresso.refresh()

        # atualiza a temperatura
        nova_temperatura = função_de_resfriamento(temperatura_atual, taxa_de_resfriamento)
        temperatura_atual = nova_temperatura
        iteração += 1

    # Encerrar a barra de progresso
    barra_de_progresso.close()

    # calcula o tempo de execução e registra
    t = time.time() - t
    registro["run_time"] = t

    # Retorna a solução
    return solução_atual, registro