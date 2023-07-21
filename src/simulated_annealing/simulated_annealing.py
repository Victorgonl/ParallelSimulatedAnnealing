import math
import tqdm
import random
import time
import multiprocessing
from typing import Any, Callable, Dict, List, Tuple

from ..knapsack_problem.knapsack import Mochila
from ..knapsack_problem.item import Item


class SimulatedAnnealing:
    def __init__(self,
                 temperatura_inicial: float,
                 temperatura_final: float,
                 taxa_resfriamento: float,
                 gerar_solucao_vizinha: Callable[[Mochila, list], Mochila],
                 comparar_solucoes: Callable[[Mochila, Mochila], int],
                 avaliar_solucao: Callable[[Mochila], int],
                 funcao_resfriamento: Callable[[float, float], float],
                 itens: List[Item],
                 solucao_inicial: Mochila = None,
                 numero_vizinhos_explorar: int = 1) -> None:
        
        self.temperatura_inicial= temperatura_inicial
        self.temperatura_final = temperatura_final
        self.taxa_resfriamento = taxa_resfriamento
        self.gerar_solucao_vizinha = gerar_solucao_vizinha
        self.comparar_solucoes = comparar_solucoes
        self.avaliar_solucao = avaliar_solucao
        self.funcao_resfriamento = funcao_resfriamento
        self.itens = itens
        self.solucao_inicial = solucao_inicial
        self.numero_vizinhos_explorar = numero_vizinhos_explorar
        
    
    def executar_sequencial(self) -> Tuple[Mochila, Dict[str, Any]]:
        
        t = time.time()

        # registro
        registro = {"avaliação": [],
                    "temperatura": [],
                    "solução": [],
                    "número_vizinhos_explorados": 0}

        # inicialização
        temperatura_atual = self.temperatura_inicial
        solucao_atual = self.solucao_inicial
        iteração = 0

        # registrar avaliação e temperatura
        registro["avaliação"].append(self.avaliar_solucao(solucao_atual))
        registro["temperatura"].append(temperatura_atual)
        registro["solução"].append(solucao_atual)

        # barra de progresso
        total = math.ceil(math.log(self.temperatura_final / self.temperatura_inicial, self.funcao_resfriamento(1, self.taxa_de_resfriamento)))
        barra_de_progresso = tqdm.tqdm(total=total, desc="Simulated Annealing",
                                    bar_format="{l_bar}{bar}| {postfix}")

        # função para explorar vizinhos
        def explorar_vizinhos(número_de_vizinhos_a_explorar,
                            vizinho_escolhido,
                            temperatura):
            for _ in range(número_de_vizinhos_a_explorar):
                solução_vizinha = self.gerar_solucao_vizinha(vizinho_escolhido[0][0], self.itens)
                erro = self.comparar_solucoes(vizinho_escolhido[0][0], solução_vizinha)
                probabilidade = math.exp(-erro / temperatura)
                if erro < 0:
                    vizinho_escolhido[0] = (solução_vizinha, erro)
                else:
                    x = random.random()
                    if probabilidade > x:
                        vizinho_escolhido[0] = (solução_vizinha, erro)
                registro["número_vizinhos_explorados"] += 1

        # laço de temperatura
        while temperatura_atual > self.temperatura_final:
            # explorar vizinhos
            vizinho_escolhido = [(solucao_atual, 0)]
            explorar_vizinhos(self.numero_vizinhos_explorar,
                            vizinho_escolhido,
                            temperatura_atual)

            # atualiza a solução atual
            solucao_atual = vizinho_escolhido[0][0]

            # chama a função de resfriamente
            nova_temperatura = self.funcao_resfriamento(temperatura_atual, self.taxa_de_resfriamento)

            # registrar avaliação e temperatura
            registro["avaliação"].append(self.avaliar_solucao(solucao_atual))
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
        return solucao_atual, registro
    

    def executar_paralelo(self,
                          forma_selecao: str = "temperature",
                          numero_processos: int = 1,
                          mostrar_barra_progresso: bool = True) -> Tuple[Mochila, Dict[str, Any]]:
        
        # inicializa a contagem de tempo
        t = time.time()

        # inicialização
        temperatura_atual = self.temperatura_inicial
        solução_atual = self.solucao_inicial
        iteração = 0
        número_vizinhos_explorar_por_preocesso = [self.numero_vizinhos_explorar // numero_processos for _ in range(numero_processos)]
        número_vizinhos_explorar_por_preocesso[-1] += self.numero_vizinhos_explorar - sum(número_vizinhos_explorar_por_preocesso)

        # registro inicial das informações
        registro = {"avaliação": [],
                    "temperatura": [],
                    "solução": [],
                    "número_vizinhos_explorados": 0}
        registro["avaliação"].append(self.avaliar_solucao(solução_atual))
        registro["temperatura"].append(temperatura_atual)
        registro["solução"].append(solução_atual)

        # barra de progresso
        if mostrar_barra_progresso:
            total = math.ceil(math.log(self.temperatura_final / self.temperatura_inicial, self.funcao_resfriamento(1, self.taxa_resfriamento)))
            barra_de_progresso = tqdm.tqdm(total=total, desc=f"Parallel Simulated Annealing - {numero_processos} processes",
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
                solução_vizinha = self.gerar_solucao_vizinha(solução_atual, self.itens)
                erro = self.comparar_solucoes(solução_atual, solução_vizinha)
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
        while temperatura_atual > self.temperatura_final:

            # explorar vizinhos
            soluções_vizinhas = multiprocessing.Manager().list()
            número_vizinhos_explorados = multiprocessing.Value("i", 0)

            # locker para processos
            lock = multiprocessing.Lock()

            # cria e inicia os processos
            processes = []
            for i in range(numero_processos):
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
            if forma_selecao == "random":
                # seleciona a solução atual como uma aleatória entre as vizinhas exploradas
                solução_atual = random.choice(soluções_vizinhas)["solução"] if soluções_vizinhas else solução_atual
            elif forma_selecao == "temperature":
                # seleciona a solução vizinha com base na temperatura
                for solução_vizinha in soluções_vizinhas:
                    x = random.random()
                    if solução_vizinha["erro"] < 0 or solução_vizinha["probabilidade"] > x:
                        solução_atual = solução_vizinha["solução"]
            elif forma_selecao == "optimal":
                # selecionado a solução atual como a vizinha de menor erro
                solução_atual = min(soluções_vizinhas, key=lambda solução_vizinha: solução_vizinha["erro"])["solução"] if soluções_vizinhas else solução_atual

            # registra as informações
            registro["número_vizinhos_explorados"] += número_vizinhos_explorados.value
            registro["avaliação"].append(self.avaliar_solucao(solução_atual))
            registro["temperatura"].append(temperatura_atual)
            registro["solução"].append(solução_atual)

            if mostrar_barra_progresso:
                # atualiza a barra de progresso
                barra_de_progresso.set_postfix({"Temperatura": "{:.5f}".format(temperatura_atual),
                                                "Avaliação": "{:.5f}".format(registro["avaliação"][-1])})
                barra_de_progresso.update(1)
                barra_de_progresso.refresh()

            # atualiza a temperatura
            nova_temperatura = self.funcao_resfriamento(temperatura_atual, self.taxa_resfriamento)
            temperatura_atual = nova_temperatura
            iteração += 1

        if mostrar_barra_progresso:
            # Encerrar a barra de progresso
            barra_de_progresso.close()

        # calcula o tempo de execução e registra
        t = time.time() - t
        registro["run_time"] = t

        # Retorna a solução
        return solução_atual, registro