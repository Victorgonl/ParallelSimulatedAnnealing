import matplotlib


def plotar_gráfico_de_dispersão(scatters,
                                title,
                                x_label, y_label):
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

def plotar_gráfico(x, y, color,
                   xlabel, ylabel, title="",
                   grid=True, xscale="linear", invert_xaxis=False):
    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(x, y, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xscale(xscale)
    ax.invert_xaxis() if invert_xaxis else None
    ax.set_ylabel(ylabel)
    ax.grid(True, which="both") if grid else None
    matplotlib.pyplot.show()