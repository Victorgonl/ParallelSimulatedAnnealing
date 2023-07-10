import math
import random
import time
import tqdm


def simulated_annealing(temperatura_inicial,
                        temperatura_final,
                        taxa_de_resfriamento,
                        gerar_solução_vizinha,
                        comparar_soluções,
                        avaliar_solução,
                        função_de_resfriamento,
                        itens,
                        solução_inicial=None,
                        número_de_vizinhos_a_explorar=1):

    t = time.time()

    # registro
    registro = {"avaliação": [],
                "temperatura": [],
                "solução": [],
                "número_vizinhos_explorados": 0}

    # inicialização
    temperatura_atual = temperatura_inicial
    solução_atual = solução_inicial
    iteração = 0

    # registrar avaliação e temperatura
    registro["avaliação"].append(avaliar_solução(solução_atual))
    registro["temperatura"].append(temperatura_atual)
    registro["solução"].append(solução_atual)

    # barra de progresso
    total = math.ceil(math.log(temperatura_final / temperatura_inicial, função_de_resfriamento(1, taxa_de_resfriamento)))
    barra_de_progresso = tqdm.tqdm(total=total, desc="Simulated Annealing",
                                   bar_format="{l_bar}{bar}| {postfix}")

    # função para explorar vizinhos
    def explorar_vizinhos(número_de_vizinhos_a_explorar,
                          vizinho_escolhido,
                          temperatura):
        for _ in range(número_de_vizinhos_a_explorar):
            solução_vizinha = gerar_solução_vizinha(vizinho_escolhido[0][0], itens)
            erro = comparar_soluções(vizinho_escolhido[0][0], solução_vizinha)
            probabilidade = math.exp(-erro / temperatura)
            if erro < 0:
                vizinho_escolhido[0] = (solução_vizinha, erro)
            else:
                x = random.random()
                if probabilidade > x:
                    vizinho_escolhido[0] = (solução_vizinha, erro)
            registro["número_vizinhos_explorados"] += 1

    # laço de temperatura
    while temperatura_atual > temperatura_final:
        # explorar vizinhos
        vizinho_escolhido = [(solução_atual, 0)]
        explorar_vizinhos(número_de_vizinhos_a_explorar,
                          vizinho_escolhido,
                          temperatura_atual)

        # atualiza a solução atual
        solução_atual = vizinho_escolhido[0][0]

        # chama a função de resfriamente
        nova_temperatura = função_de_resfriamento(temperatura_atual, taxa_de_resfriamento)

        # registrar avaliação e temperatura
        registro["avaliação"].append(avaliar_solução(solução_atual))
        registro["temperatura"].append(temperatura_atual)

        # atualiza a barra de progresso
        barra_de_progresso.set_postfix({"Temperatura": "{:.5f}".format(temperatura_atual),
                                        "Avaliação": "{:.5f}".format(registro["avaliação"][-1])})
        barra_de_progresso.update(1)
        barra_de_progresso.refresh()

        # atualiza a temperatura
        temperatura_atual = nova_temperatura
        iteração += 1

    # encerra a barra de progresso
    barra_de_progresso.close()

    t = time.time() - t
    registro["run_time"] = t

    # retorna a solução
    return solução_atual, registro