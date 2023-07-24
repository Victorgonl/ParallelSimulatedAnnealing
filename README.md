<center>

<img src="./figs/UFLA.png" width=400>

# Parallel Simulated Annealing

</center>

Trabalho Final da disciplina **Programação Paralela e Concorrente** (2023/1).

**Professora:** Marluce Rodrigues Pereira

**Alunos:**

- João Gabriel Kondarzewski Zanella - 202020091
- Henrique Curi de Miranda - 202020087
- Victor Gonçalves Lima - 202020775

O trabalho tem como objetivo paralelizar o algorimo de otimização ***Simulated Annealing*** e analizar os resutados obtidos.

---

<center>
<figure id="fig1">
  <img src="./figs/Hill_Climbing_with_Simulated_Annealing.gif">
  <figcaption>Figura 1: Simulated annealing procurando pelo máximo global. Quanto menor a temperatura, menor a chance de escolher uma solução pior.</figcaption>
</figure>
</center>

---

Para mais informações sobre o algoritmo: https://en.wikipedia.org/wiki/Simulated_annealing

## Ambiente de desenvolvimento

### Informações

- Sistema Operacional: Linux (distribuições baseadas em Debian)

- Linguagem de Programação: Python (3.10)

### Pacotes necessários

Para criação do ambiente virtual com `venv`, é ncesserário que os pacotes `python3-pip` e `python3-venv` estejam deviamente instalados.

    sudo apt install python3-pip

<p></p>

    sudo apt install python3-venv


### Ambiente virtual Python (venv)

A criação e ativação do ambiente virtual Python são realizadas, respecivamente, pelos comandos:

    python3 -m venv venv

<p></p>

    source venv/bin/activate

### Pacotes Python (pip)

Os pacotes `pip` estão disponíveis no arquivo `requirements.txt` e podem ser instalados (após estar dentro do `venv`) com:

    pip install -r requirements.txt