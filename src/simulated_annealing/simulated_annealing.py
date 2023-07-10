import copy
import math
import random
import time
import tqdm
import numpy


def simulated_annealing(temperatura_inicial,
                        temperatura_final,
                        taxa_de_resfriamento,
                        gerar_solução_vizinha,
                        comparar_soluções,
                        avaliar_solução,função_de_resfriamento,
                        itens,
                        gerar_solução_inicial=None,
                        solução_inicial=None,
                        número_de_vizinhos_explorados=1):
    # registro
    registro = {"avaliação": [],
                "temperaturas": [],
                "probabilidades": [],
                "erro": []}

    # inicializão
    if solução_inicial is None and not gerar_solução_inicial is None:
        solução_inicial = gerar_solução_inicial()
    temperatura_atual = temperatura_inicial
    solução_atual = copy.deepcopy(solução_inicial)
    iteração = 0

    # barra de progresso
    total=temperatura_inicial-temperatura_final
    barra_de_progresso = tqdm.tqdm(total=total, desc="Simulated Annealing",
                                   bar_format="{l_bar}{bar}| {postfix}")

    # laço de temperatura
    while temperatura_atual > temperatura_final:
        # explorar vizinhos
        vizinho_escolhido = None
        for _ in range(número_de_vizinhos_explorados):
            solução_vizinha = gerar_solução_vizinha(solução_atual, itens)
            erro = comparar_soluções(solução_atual, solução_vizinha)
            probabilidade = math.exp(-erro / temperatura_atual)

            # registrar avaliação e temperatura
            registro["avaliação"].append(avaliar_solução(solução_atual))
            registro["temperaturas"].append(temperatura_atual)
            registro["erro"].append(erro)
            registro["probabilidades"].append(probabilidade) if probabilidade < 1.0 else registro["probabilidades"].append(numpy.NAN)

            if erro < 0:
                vizinho_escolhido = copy.deepcopy(solução_vizinha)
            else:
                x = random.random()
                if probabilidade > x:
                    vizinho_escolhido = copy.deepcopy(solução_vizinha)
                else:
                    pass

        # atualiza a solução atual se solução vizinha for válida
        solução_atual = vizinho_escolhido if vizinho_escolhido is not None else solução_atual

        # chama a função de resfriamente
        nova_temperatura = função_de_resfriamento(temperatura_atual, taxa_de_resfriamento)

        # atualiza a barra de progresso
        barra_de_progresso.set_postfix({"Temperatura": "{:.5f}".format(temperatura_atual),
                                        "Avaliação": "{:.5f}".format(registro["avaliação"][-1])})
        barra_de_progresso.update(temperatura_atual-nova_temperatura)
        barra_de_progresso.refresh()

        # atualiza a temperatura
        temperatura_atual = nova_temperatura
        iteração += 1

    # encerra a barra de progresso
    barra_de_progresso.close()
    time.sleep(1)

    # retorna a solução
    return solução_atual, registro