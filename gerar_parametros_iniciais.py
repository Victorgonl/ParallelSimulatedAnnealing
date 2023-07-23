from src.funcoes_auxiliares import gerar_itens_aleatorios, gerar_mochila_aleatoria
from src.funcoes_registro import registrar_populacao, registrar_solucao_inicial


if __name__ == "__main__":

    parametros_populacao = {"numero_itens": 10000,  # número de itens que serão gerados
                                "valor_minimo": 1,      # prioridade mínima
                                "valor_maximo": 5,      # prioridade máxima
                                "tipo_valor": "int",    # tipo dos valores
                                "peso_minimo": 10.0,    # 10 kgs
                                "peso_maximo": 1000.0,  # 1 tonelada
                                "tipo_peso": "float"}   # tipo dos pesos

    itens = gerar_itens_aleatorios(parametros_populacao["numero_itens"],
                                    parametros_populacao["valor_minimo"],
                                    parametros_populacao["valor_maximo"],
                                    parametros_populacao["tipo_valor"],
                                    parametros_populacao["peso_minimo"],
                                    parametros_populacao["peso_maximo"],
                                    parametros_populacao["tipo_peso"])

    mochila_inicial = gerar_mochila_aleatoria(capacidade=10000.0, itens=itens)

    registrar_populacao(parametros_populacao, itens, "./parametros_iniciais/", True)

    registrar_solucao_inicial(mochila_inicial, "./parametros_iniciais/",)

