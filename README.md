# :chart_with_upwards_trend: Simulador De Mercado :chart_with_downwards_trend:
Esse é um ambicioso projeto que simula o comportamento do mercado utilizando ferramentas provenientes de leis Físicas em Python.

## Sumário

* [Simulação de Opções Binárias e o "Andar do Bêbado"](#simulação-de-opções-binárias-e-o-andar-do-bêbado)
   * [Objetivo](#objetivo)
   * [Inspiração](#inspiração)
   * [Relação com o código](#relação-com-o-código)
   * [Detalhes do código](#detalhes-do-código)
   * [Código 1](#código-1)
   * [Output 1](#output-1)
   * [Considerações](#considerações)
* [Distibuição de Probabilidades dos Saldos Finais](#distibuição-de-probabilidades-dos-saldos-finais)
   * [Base Teórica](#base-teórica)
   * [Código 2](#código-2)
   * [Output 2](#output-2)
* [Implementação de Candles em Gráficos Interativos](#implementação-de-candles-em-gráficos-interativos)
   * [Introdução ao Plotly](#introdução-ao-plotly)
   * [O passo aleatório](#o-passo-aleatório)
   * [Entrada e Saída dos Candles](#entrada-e-saída-dos-candles)
   * [Máximos e Mínimos dos Candles](#máximos-e-mínimos-dos-candles)
   * [Indicador de Volume de Mercado](#indicador-de-volume-de-mercado)
   * [Médias Móveis e Bandas de Bollinger](#médias-móveis-e-bandas-de-bollinger)
   * [Indicador RSI](#indicador-rsi)
   * [Código 3](#código-3)
   * [Output 3](#output-3)
* [Geração de Gráficos em Tempo Real](#geração-de-gráficos-em-tempo-real)
   * [Introdução ao Dash](#introdução-ao-dash)

# Simulação de Opções Binárias e o "Andar do Bêbado"

Primeiramente, vamos começar com o mais simples, que é simular gráficos de opções binárias, onde a chance de lucrar, em teoria, se equipara a chance de ter um prejuízo.

## **Objetivo**

Simular o desempenho de uma estratégia de opções binárias com base no conceito do "andar do bêbado", um modelo probabilístico que ilustra o movimento aleatório de uma partícula.

## **Inspiração**

O "andar do bêbado" foi utilizado por Albert Einstein para explicar o movimento browniano, o movimento aleatório de partículas em suspensão em um fluido. A ideia é que a partícula se move em uma série de passos aleatórios, cada um com a mesma probabilidade de ser para frente ou para trás.

## **Relação com o código**

No código Python, simulamos uma série de operações de opções binárias, onde cada operação tem uma probabilidade fixa de ser vencedora ou perdedora. O movimento do saldo ao longo das operações é similar ao "andar do bêbado", com oscilações aleatórias em torno de um valor central.

## **Detalhes do código**

Antes, vou explicar como o código funciona.

* **Parâmetros:**
    * `qtde`: Número de simulações a serem realizadas.
    * `n`: Número de operações por simulação.
    * `stop`: Limite de stop loss (perda máxima).
    * `profit`: Limite de take profit (lucro máximo).
    * `t`: Porcentagem de acerto nas operações (fixado em 50% neste exemplo).

* **Funções:**
    * `resultado`: Analisa os resultados das simulações e conta quantas vezes cada resultado (stop loss, take profit ou nenhum) ocorreu.
    * `f`: Simula uma única série de operações de opções binárias.
    * `rnd`: Gera uma lista de números aleatórios para simular os movimentos de preço.

* **Simulação e plotagem:**
    * 8 simulações são realizadas e plotadas no mesmo gráfico.
    * O saldo final de cada simulação é armazenado na lista `saldo`.

* **Resultados:**
    * A função `resultado` imprime a quantidade de simulações que resultaram em stop loss, take profit ou nenhum dos dois.

## **Código 1**
```python
import matplotlib.pyplot as plt  # Biblioteca de plotagem
import numpy as np  # Biblioteca de computação numérica

# Parâmetros da simulação
qtde = 1000  # Número de simulações
n = 1000  # Número de operações por simulação
stop = -2000  # Limite de stop loss
profit = 2000  # Limite de take profit

# Entrada de dados (opcional)
#t = float(input("% de acerto:"))
t = 50  # Porcentagem de acerto (fixado para 50 neste exemplo)

def resultado(saldo, qtde, stop, profit):
    """
    Analisa os resultados das simulações e conta quantas vezes cada 
    resultado (stop loss, take profit ou nenhum) ocorreu.
    
    Argumentos:
        saldo: Lista com os saldos finais de cada simulação.
        qtde: Número de simulações.
        stop: Limite de stop loss.
        profit: Limite de take profit.
    Retorno:
        Lista com a contagem de cada tipo de resultado.
    """
    stoploss = 0
    nothing = 0
    takeprofit = 0
    for i in range(qtde):
        if saldo[i] <= stop:
            stoploss += 1
        elif saldo[i] >= profit:
            takeprofit += 1
        else:
            nothing += 1
        resultado = [stoploss, takeprofit, nothing]
    return resultado

def f(y, t, n, stop, profit):
    """
    Simula uma única série de operações de opções binárias.
    
    Argumentos:
        y: Lista com os movimentos de preço aleatórios.
        t: Porcentagem de acerto.
        n: Número de operações.
        stop: Limite de stop loss.
        profit: Limite de take profit.
        
    Retorno:
        Lista com o saldo ao longo da simulação.
    """
    valor_investido = 50
    f = np.zeros(n)
    f[0] = 0
    for i in range(n-1):
        # Ajusta o saldo de acordo com a operação e o resultado
        if f[i] > stop and f[i] < profit:
            if y[i] > t:
                f[i+1] = f[i] - valor_investido
            else:
                f[i+1] = f[i] + valor_investido
        # Se o limite for atingido, interrompe a simulação
        else:
            if f[i] <= stop:
                for j in range(i,n):
                    f[j] = stop
            elif f[i] >= profit:
                for j in range(i,n):
                    f[j] = profit
            i=n
    return f

def rnd(s):
    """
    Gera uma lista de números aleatórios para simular os movimentos de preço.
    
    Argumentos:
        s: Tamanho da lista.
        
    Retorno:
        Lista com números aleatórios.
    """
    a = np.random.randint(102, size=s)
    b = []
    for i in range(s):
        b.append(a[i])
    return b

x = np.arange(0, n, 1)  # Eixo X para o gráfico (número de operações)
y = np.zeros(n)  # Linha de base para o gráfico

plt.plot(x, y, color='black')  # Plota a linha de base

# Simula 8 cenários e plota o saldo em cada um
for _ in range(8):
    plt.plot(x, f(rnd(n), t, n, stop, profit), linewidth=0.7)

plt.xlabel('Número de operações')  # Título do eixo X
plt.ylabel('Saldo (R$)')  # Título do eixo Y
plt.title('Simulação de opções binárias')  # Título do gráfico
plt.style.use('dark_background') # Tema do Gráfico
plt.show()  # Exibe o gráfico

# A lista saldo armazena o saldo final de cada uma das qtde simulações
saldo = [] 
for i in range(qtde): 
    saldo.append(f(rnd(n), t, n, stop, profit)[n-1]) 
    # Armazena o saldo final de cada simulação

r = resultado(saldo, qtde, stop, profit)
# Mostra a quantidade de simulações que terminaram em cada um dos cenários.
print("Qtde. Stop Loss:", r[0])
print("Qtde. Take Profit:", r[1])
print("Nem um nem outro:", r[2])
```

## **Output 1**

<img src="https://github.com/Geovannisz/SimuladorDeMercado/assets/82838501/d74dbb37-9909-4f96-8907-16b505b7b7c8">

`Qtde. Stop Loss: 205` `Qtde. Take Profit: 216` `Nem um nem outro: 579`

## **Considerações:**

* O código serve como um exemplo e pode ser adaptado para diferentes cenários.
* Para uma análise mais completa, é recomendável realizar simulações com diferentes parâmetros e avaliar a sensibilidade dos resultados.
* É possível adicionar um loop para realizar simulações com diferentes valores de `t` (porcentagem de acerto) e analisar o impacto na quantidade de stop losses, take profits e resultados intermediários.

# Distibuição de Probabilidades dos Saldos Finais



## Base Teórica



## Código 2



## Output 2



# Implementação de Candles em Gráficos Interativos



## Introdução ao Plotly



## O passo aleatório



## Entrada e Saída dos Candles



## Máximos e Mínimos dos Candles



## Indicador de Volume de Mercado



## Médias Móveis e Bandas de Bollinger



## Indicador RSI



## Código 3



## Output 3



# Geração de Gráficos em Tempo Real



## Introdução ao Dash

