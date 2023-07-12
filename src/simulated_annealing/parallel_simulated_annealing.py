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
                                 forma_de_seleção="temperature",
                                 número_de_processos=1,
                                 mostrar_barra_de_progresso=True):

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
    if mostrar_barra_de_progresso:
        total = math.ceil(math.log(temperatura_final / temperatura_inicial, função_de_resfriamento(1, taxa_de_resfriamento)))
        barra_de_progresso = tqdm.tqdm(total=total, desc=f"Parallel Simulated Annealing - {número_de_processos} processes",
                                    bar_format="{l_bar}{bar}| {postfix}")

    # função para explorar vizinhos
    def explorar_vizinhos(lock,
                          process_id,
                          soluções_vizinhas,
                          número_vizinhos_explorar,
                          número_vizinhos_explorados):
        vizinhos_explorados = []
        i = 0
        for _ in range(número_vizinhos_explorar):
            solução_vizinha = gerar_solução_vizinha(solução_atual, itens)
            erro = comparar_soluções(solução_atual, solução_vizinha)
            probabilidade = math.exp(-erro / temperatura_atual)
            if erro < 0:
                    vizinhos_explorados.append({"solução": solução_vizinha,
                                                "erro": erro,
                                                "probabilidade": probabilidade})
            else:
                x = random.random()
                if probabilidade > x:
                    vizinhos_explorados.append({"solução": solução_vizinha,
                                                "erro": erro,
                                                "probabilidade": probabilidade})
            i += 1
        with lock:
            soluções_vizinhas += vizinhos_explorados
            número_vizinhos_explorados.value += i

    # laço de temperatura
    while temperatura_atual > temperatura_final:

        # explorar vizinhos
        soluções_vizinhas = multiprocessing.Manager().list()
        número_vizinhos_explorados = multiprocessing.Value("i", 0)

        # locker para processos
        lock = multiprocessing.Lock()

        # cria e inicia os processos
        processes = []
        for i in range(número_de_processos):
            process = multiprocessing.Process(target=explorar_vizinhos, args=(lock,
                                                                              i,
                                                                              soluções_vizinhas,
                                                                              número_vizinhos_explorar_por_preocesso[i],
                                                                              número_vizinhos_explorados))
            processes.append(process)
            process.start()

        # sincroniza os processos
        for process in processes:
            process.join()

        # encerra os processos
        for process in processes:
            process.close()

        # atualiza a solução atual de acordo com a forma de seleção
        if forma_de_seleção == "random":
            # seleciona a solução atual como uma aleatória entre as vizinhas exploradas
            solução_atual = random.choice(soluções_vizinhas)["solução"] if soluções_vizinhas else solução_atual
        elif forma_de_seleção == "temperature":
            # seleciona a solução vizinha com base na temperatura
            for solução_vizinha in soluções_vizinhas:
                x = random.random()
                if solução_vizinha["erro"] < 0 or solução_vizinha["probabilidade"] > x:
                    solução_atual = solução_vizinha["solução"]
        elif forma_de_seleção == "optimal":
            # selecionado a solução atual como a vizinha de menor erro
            solução_atual = min(soluções_vizinhas, key=lambda solução_vizinha: solução_vizinha["erro"])["solução"] if soluções_vizinhas else solução_atual

        # registra as informações
        registro["número_vizinhos_explorados"] += número_vizinhos_explorados.value
        registro["avaliação"].append(avaliar_solução(solução_atual))
        registro["temperatura"].append(temperatura_atual)
        registro["solução"].append(solução_atual)

        if mostrar_barra_de_progresso:
            # atualiza a barra de progresso
            barra_de_progresso.set_postfix({"Temperatura": "{:.5f}".format(temperatura_atual),
                                            "Avaliação": "{:.5f}".format(registro["avaliação"][-1])})
            barra_de_progresso.update(1)
            barra_de_progresso.refresh()

        # atualiza a temperatura
        nova_temperatura = função_de_resfriamento(temperatura_atual, taxa_de_resfriamento)
        temperatura_atual = nova_temperatura
        iteração += 1

    if mostrar_barra_de_progresso:
        # Encerrar a barra de progresso
        barra_de_progresso.close()

    # calcula o tempo de execução e registra
    t = time.time() - t
    registro["run_time"] = t

    # Retorna a solução
    return solução_atual, registro