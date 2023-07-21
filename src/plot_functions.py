from typing import Any
import matplotlib.pyplot

from .helper_functions import avaliar_mochila


def plotar_grafico_de_dispersao(scatters,
                                title,
                                x_label,
                                y_label) -> None:
    
    if not type(scatters) is list:
        scatters = [scatters]
    fig, ax = matplotlib.pyplot.subplots()
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    for scatter in scatters:
        ax.scatter(scatter["x"],
                   scatter["y"],
                   s=scatter["s"],
                   color=scatter["color"],
                   label=scatter["label"])
    ax.legend(loc="center right")
    matplotlib.pyplot.show()
    

def plotar_grafico(x,
                   y,
                   color,
                   xlabel,
                   ylabel,
                   title="",
                   grid=True,
                   xscale="linear",
                   invert_xaxis=False) -> None:
    
    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(x, y, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xscale(xscale)
    ax.invert_xaxis() if invert_xaxis else None
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both") if grid else None
    matplotlib.pyplot.show()


def plotar_itens(itens, mochila=None) -> None:
    itens_dict = {
        "item": [item.id for item in itens],
        "valor": [item.valor for item in itens],
        "peso": [item.peso for item in itens],
    }
    scatter_itens = {"x": [item.peso for item in itens],
                    "y": [item.valor for item in itens],
                    "s": 1,
                    "label": "Itens",
                    "color": "darkblue"}
    if mochila is None:
        plotar_grafico_de_dispersao(scatter_itens,
                                    title="Gráfico de Dispersão dos Itens",
                                    x_label="peso", y_label="valor")
    else:
        scatter_mochila = {"x": [item.peso for item in mochila.itens],
                           "y": [item.valor for item in mochila.itens],
                           "s": 3,
                           "label": "Itens selecionados",
                           "color": "orangered"}
        print("Total de itens na mochila:", len(mochila.itens))
        print("Valor total na mochila:", avaliar_mochila(mochila))
        print("Peso total na mochila:", mochila.peso())
        plotar_grafico_de_dispersao([scatter_itens, scatter_mochila],
                                    "Itens selecionados na mochila",
                                    x_label="Peso", y_label="Valor")