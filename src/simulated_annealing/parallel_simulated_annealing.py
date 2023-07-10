import copy
import math
import tqdm
import numpy
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
                        gerar_solução_inicial=None,
                        solução_inicial=None,
                        número_de_vizinhos_a_explorar=1,
                        número_de_threads=1):
    # Registro
    registro = {
        "avaliação": [],
        "temperaturas": [],
        "número_vizinhos_explorados": 0
    }

    # inicialização
    if solução_inicial is None and gerar_solução_inicial is not None:
        solução_inicial = gerar_solução_inicial()
    temperatura_atual = temperatura_inicial
    solução_atual = copy.deepcopy(solução_inicial)
    iteração = 0

    # registrar avaliação e temperatura
    registro["avaliação"].append(avaliar_solução(solução_atual))
    registro["temperaturas"].append(temperatura_atual)

    # barra de progresso
    total = math.ceil(math.log(temperatura_final / temperatura_inicial, função_de_resfriamento(1, taxa_de_resfriamento)))
    barra_de_progresso = tqdm.tqdm(total=total, desc="Parallel Simulated Annealing",
                                   bar_format="{l_bar}{bar}| {postfix}")

    # função para explorar vizinhos
    def explorar_vizinhos(número_de_vizinhos_a_explorar,
                          vizinhos_escolhidos,
                          temperatura,
                          thread_id):
        for _ in range(número_de_vizinhos_a_explorar):
            solução_vizinha = gerar_solução_vizinha(vizinhos_escolhidos_por_thread[thread_id][0], itens)
            erro = comparar_soluções(vizinhos_escolhidos_por_thread[thread_id][0], solução_vizinha)
            probabilidade = math.exp(-erro / temperatura)
            if erro < 0:
                vizinhos_escolhidos_por_thread[thread_id] = (solução_vizinha, erro)
            else:
                x = random.random()
                if probabilidade > x:
                    vizinhos_escolhidos[thread_id] = (solução_vizinha, erro)
            registro["número_vizinhos_explorados"] += 1

    # laço de temperatura
    while temperatura_atual > temperatura_final:
        # explorar vizinhos
        threads = []
        vizinhos_escolhidos_por_thread = [(solução_atual, 0) for _ in range(número_de_threads)]
        número_de_vizinhos_a_explorar_por_thread = [número_de_vizinhos_a_explorar // número_de_threads for _ in range(número_de_threads)]
        número_de_vizinhos_a_explorar_por_thread[-1] += número_de_vizinhos_a_explorar - sum(número_de_vizinhos_a_explorar_por_thread)

        for i in range(número_de_threads):
            t = threading.Thread(target=explorar_vizinhos, args=(número_de_vizinhos_a_explorar_por_thread[i], vizinhos_escolhidos_por_thread, temperatura_atual, len(threads)))
            threads.append(t)
            t.start()

        # Aguardar até que todas as threads terminem
        for t in threads:
            t.join()

        # Selecionar a solução atual como a solução vizinha com o menor erro
        solução_atual, erro = min(vizinhos_escolhidos_por_thread, key=lambda x: x[1])

        # Chamar a função de resfriamento
        nova_temperatura = função_de_resfriamento(temperatura_atual, taxa_de_resfriamento)

        # Registrar avaliação e temperatura
        registro["avaliação"].append(avaliar_solução(solução_atual))
        registro["temperaturas"].append(temperatura_atual)

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
    time.sleep(1)

    # Retorna a solução
    return solução_atual, registro