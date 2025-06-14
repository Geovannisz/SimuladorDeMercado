<!--
<details>
<summary>Click to expand</summary>

This is the content of the collapsible section. You can include any Markdown-formatted text, lists, or code here.
-->


# :chart_with_upwards_trend: Simulador De Mercado :chart_with_downwards_trend:
Esse é um ambicioso projeto que simula o comportamento do mercado utilizando ferramentas provenientes de leis Físicas em Python.

## Sumário

* [Simulação de Opções Binárias e o \"Andar do Bêbado\"](#simulação-de-opções-binárias-e-o-andar-do-bêbado)
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

O "Andar do Bêbado" foi utilizado por Albert Einstein para explicar o movimento browniano, o movimento aleatório de partículas em suspensão em um fluido. A ideia é que a partícula se move em[...]

## **Relação com o código**

No código Python, simulamos uma série de operações de opções binárias, onde cada operação tem uma probabilidade fixa de ser vencedora ou perdedora. O movimento do saldo ao longo das opera[...]

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
* É possível adicionar um loop para realizar simulações com diferentes valores de `t` (porcentagem de acerto) e analisar o impacto na quantidade de stop losses, take profits e resultados inte[...]

# Distibuição de Probabilidades dos Saldos Finais

Vamos voltar a analogia do "Andar do Bêbado". Com o tempo, a distância total percorrida pelo bêbado será a soma dos passos individuais. Como os passos são aleatórios, não há como prever e[...]

A probabilidade de o bêbado estar a uma distância específica do ponto de partida segue uma função gaussiana, também conhecida como distribuição normal. Essa função tem a forma de um sin[...]
Continuando a analogia do "Andar do Bêbado", vimos que, com o tempo, a distância total percorrida pelo bêbado é a soma de passos aleatórios. Embora não possamos prever a trajetória exata de uma única simulação, podemos analisar a distribuição dos resultados finais de *muitas* simulações.

A teoria sugere que, para um grande número de passos (ou operações, no nosso caso), a distribuição das posições finais (saldos) do "bêbado" se aproxima de uma **distribuição normal (ou Gaussiana)**. Esta distribuição é caracterizada por sua forma de sino, onde a maioria dos resultados se concentra em torno da média, e resultados mais extremos se tornam progressivamente menos prováveis.

No contexto da simulação de mercado com 50% de chance de acerto e sem taxas, a média esperada do saldo final, após muitas operações, tende a zero (desconsiderando os limites de stop/profit por um momento para a análise da distribuição subjacente). O `Código 2` demonstrará isso visualmente.

## Base Teórica

Partindo da posição $x_0 = 0$, o bêbado pode dar $1$ passo, fazendo com que sua posição $x_1$ possa ser $1$ ou $-1$. Logo:

$$ x_1 = x_0 \pm 1 $$

A média das posições de $x_1$ será de:

$$ \langle x_1\rangle = \dfrac{-1 + 1}{2} = 0 $$

Já a média quadrada de $x_1$ será:

$$ \langle (x_1)^2\rangle = \dfrac{(-1)^2 + (1)^2}{2} = 1 $$

Agora, ao dar o passo $2$, teremos:


\begin{align*}

\langle x_2\rangle &= 0\\

\langle (x_2)^2\rangle &= \langle (x_1 \pm 1)^2\rangle = 1$$

\end{align*}

## Código 2
Este código irá simular um grande número de "passeios aleatórios" (semelhantes aos do `Código 1`, mas focando apenas nos saldos finais) e plotará um histograma desses saldos. Isso nos permitirá observar a forma da distribuição.

```python
import matplotlib.pyplot as plt
import numpy as np

# Parâmetros da simulação
qtde_simulacoes = 10000  # Número de simulações para observar a distribuição
n_operacoes = 500      # Número de operações por simulação
valor_investido = 50   # Valor para cada operação (ganho ou perda)
prob_acerto = 0.50     # Probabilidade de ganhar uma operação (50%)

def simular_um_passeio(n_ops, val_inv, prob_ac):
    """Simula um único passeio aleatório (série de operações)."""
    saldo = 0
    for _ in range(n_ops):
        if np.random.rand() < prob_ac:
            saldo += val_inv  # Ganhou
        else:
            saldo -= val_inv  # Perdeu
    return saldo

# Armazena os saldos finais de todas as simulações
saldos_finais = []
for _ in range(qtde_simulacoes):
    saldos_finais.append(simular_um_passeio(n_operacoes, valor_investido, prob_acerto))

# Plotando o histograma dos saldos finais
plt.figure(figsize=(10, 6))
plt.hist(saldos_finais, bins=50, density=True, color='skyblue', edgecolor='black', alpha=0.7)

# Adicionando uma curva de densidade (KDE) para melhor visualização da forma
# (Requer scipy.stats.gaussian_kde, opcional)
try:
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(saldos_finais)
    x_range = np.linspace(min(saldos_finais), max(saldos_finais), 500)
    plt.plot(x_range, kde(x_range), color='red', linewidth=2, label='Estimativa de Densidade (KDE)')
    plt.legend()
except ImportError:
    print("Scipy não instalado. A curva KDE não será plotada.")


plt.title(f'Distribuição dos Saldos Finais após {n_operacoes} Operações ({qtde_simulacoes} Simulações)')
plt.xlabel('Saldo Final (R$)')
plt.ylabel('Densidade de Probabilidade')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.style.use('dark_background')
plt.show()

media_saldos = np.mean(saldos_finais)
desvio_padrao_saldos = np.std(saldos_finais)

print(f"Média dos saldos finais: R$ {media_saldos:.2f}")
print(f"Desvio padrão dos saldos finais: R$ {desvio_padrao_saldos:.2f}")
```

## Output 2
O output esperado para o `Código 2` é um gráfico de histograma. Este histograma representará a frequência (ou densidade de probabilidade) dos diferentes saldos finais obtidos após `n_operacoes` em cada uma das `qtde_simulacoes`.

Visualmente, o histograma deve apresentar:
*   Uma concentração maior de resultados próximos ao saldo zero (já que a probabilidade de acerto é de 50% e não há viés).
*   Uma forma que se assemelha a uma **curva de sino (distribuição normal)**, simétrica em torno da média.
*   As "caudas" da distribuição mostrarão que saldos finais muito positivos ou muito negativos são menos frequentes.
*   Se a biblioteca `scipy` estiver disponível, uma curva de estimativa de densidade do kernel (KDE) será sobreposta ao histograma, suavizando a forma da distribuição e tornando a semelhança com a curva normal mais evidente.

Além do gráfico, serão impressos no console:
*   A média dos saldos finais, que deve ser próxima de zero.
*   O desvio padrão dos saldos finais, que quantifica a dispersão dos resultados em torno da média.

# Implementação de Candles em Gráficos Interativos

Até agora, simulamos a trajetória do saldo. No mercado financeiro real, a variação de preços dos ativos é comumente visualizada através de **gráficos de candlestick (ou velas)**. Cada "vela" representa a movimentação de preços durante um intervalo de tempo específico (e.g., um minuto, uma hora, um dia) e encapsula quatro informações cruciais:

1.  **Preço de Abertura (Open):** O preço no início do intervalo.
2.  **Preço de Fechamento (Close):** O preço no final do intervalo.
3.  **Preço Máximo (High):** O maior preço atingido durante o intervalo.
4.  **Preço Mínimo (Low):** O menor preço atingido durante o intervalo.

A cor da vela geralmente indica se o preço subiu (fechamento > abertura) ou desceu (fechamento < abertura).

## Introdução ao Plotly

Para criar gráficos de candlestick interativos e visualmente ricos, utilizaremos a biblioteca **Plotly**. Plotly é uma biblioteca de visualização de dados para Python que permite criar uma ampla gama de gráficos interativos e de qualidade de publicação. Seus gráficos são renderizados usando HTML e JavaScript, o que os torna ideais para dashboards web e notebooks Jupyter.

Vantagens do Plotly para este projeto:
*   **Interatividade:** Permite zoom, pan, visualização de valores ao passar o mouse (tooltips), e mais.
*   **Gráficos Financeiros:** Possui suporte nativo para gráficos de candlestick e outros tipos de gráficos financeiros.
*   **Customização:** Oferece amplas opções para customizar a aparência dos gráficos.
*   **Integração:** Funciona bem com Pandas DataFrames e pode ser facilmente integrado com Dash para criar dashboards.

## O passo aleatório

A base para simular a formação dos preços que comporão nossos candles ainda será o conceito do "passo aleatório" ou "andar do bêbado". Podemos simular uma série temporal de preços onde cada novo preço é o preço anterior mais uma variação aleatória (positiva ou negativa).

$P_{t} = P_{t-1} + \Delta P_{aleatório}$

Essa série de preços servirá como base para definir os preços de fechamento dos nossos candles.

## Entrada e Saída dos Candles

Para um determinado período (candle):
*   O **preço de abertura (Open)** do candle atual é geralmente o **preço de fechamento (Close)** do candle anterior. Para o primeiro candle, podemos definir um preço de abertura inicial.
*   O **preço de fechamento (Close)** do candle atual é o preço da nossa série simulada ao final do período que o candle representa.

## Máximos e Mínimos dos Candles

Dentro de cada período que um candle representa, o preço não se move linearmente da abertura para o fechamento; ele flutua.
*   O **preço máximo (High)** é o ponto mais alto que o preço atingiu durante o período do candle.
*   O **preço mínimo (Low)** é o ponto mais baixo que o preço atingiu durante o período do candle.

Em nossa simulação, após definir o Open e o Close, podemos gerar o High e o Low adicionando/subtraindo um fator de volatilidade aleatório, garantindo que:
`Low <= min(Open, Close)` e `High >= max(Open, Close)`.

## Indicador de Volume de Mercado

O **volume** representa a quantidade de um ativo que foi negociada durante o período do candle. É um indicador importante da força ou convicção por trás de um movimento de preço.
*   **Alto volume** em um movimento de alta pode indicar forte pressão compradora.
*   **Alto volume** em um movimento de baixa pode indicar forte pressão vendedora.

Em nossa simulação, podemos gerar valores de volume sintéticos, talvez com alguma aleatoriedade e, opcionalmente, correlacionando-os com a magnitude da variação do preço no candle (candles com maior variação de preço podem ter um volume maior).

## Médias Móveis e Bandas de Bollinger

**Médias Móveis (Moving Averages - MA):** Suavizam os dados de preço para ajudar a identificar a direção da tendência. Uma Média Móvel Simples (SMA) é calculada como a média dos preços de fechamento durante um número específico de períodos anteriores.
*   Exemplo: SMA de 20 períodos (SMA20) é a média dos últimos 20 preços de fechamento.

**Bandas de Bollinger (Bollinger Bands):** São um indicador de volatilidade que consiste em:
1.  Uma Média Móvel Simples (geralmente no centro).
2.  Uma banda superior: SMA + (K * Desvio Padrão dos preços).
3.  Uma banda inferior: SMA - (K * Desvio Padrão dos preços).
    *   'K' é um multiplicador, comumente 2.
    *   O desvio padrão é calculado sobre os preços usados para a SMA.

As bandas se alargam quando a volatilidade aumenta e se estreitam quando a volatilidade diminui. Preços tocando as bandas podem indicar condições de sobrecompra (banda superior) ou sobrevenda (banda inferior).

## Indicador RSI

O **RSI (Relative Strength Index - Índice de Força Relativa)** é um oscilador de momento que mede a velocidade e a mudança dos movimentos de preços. Ele varia de 0 a 100.
*   Tradicionalmente, o RSI é considerado **sobrecomprado** quando está acima de 70 e **sobrevendido** quando está abaixo de 30.
*   Ele compara a magnitude dos ganhos recentes com as perdas recentes durante um período específico (comumente 14 períodos) para determinar se um ativo está sobrecomprado ou sobrevendido.

O cálculo envolve:
1.  Calcular os ganhos médios e as perdas médias durante o período.
2.  Calcular a Força Relativa (RS) = Ganhos Médios / Perdas Médias.
3.  Calcular o RSI = 100 - (100 / (1 + RS)).

## Código 3
Este código irá:
1.  Gerar uma série temporal de preços usando um passo aleatório.
2.  Construir dados OHLC (Open, High, Low, Close) e Volume para cada candle.
3.  Calcular uma Média Móvel Simples (SMA).
4.  Calcular Bandas de Bollinger.
5.  Calcular o RSI.
6.  Usar Plotly para criar um gráfico de candlestick interativo com esses indicadores.

```python
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

# Parâmetros da simulação de preços e candles
num_candles = 200
preco_inicial = 100
volatilidade_diaria = 0.02 # Percentual de volatilidade para simular H/L
volatilidade_passo = 0.01 # Percentual para o passo aleatório do preço de fechamento

# Períodos para os indicadores
periodo_sma = 20
periodo_rsi = 14
num_desvios_bollinger = 2

# 1. Gerar preços de fechamento (Close) com passo aleatório
precos_close = [preco_inicial]
for _ in range(1, num_candles):
    movimento = precos_close[-1] * volatilidade_passo * np.random.normal() # Movimento gaussiano
    novo_preco = precos_close[-1] + movimento
    precos_close.append(max(novo_preco, 0.01)) # Evitar preços negativos

df = pd.DataFrame({'Close': precos_close})
df.index = pd.to_datetime(pd.date_range(start='2023-01-01', periods=num_candles)) # Adicionar um índice de tempo

# 2. Construir dados OHLC e Volume
df['Open'] = df['Close'].shift(1)
df.loc[df.index[0], 'Open'] = preco_inicial # Definir o primeiro Open

# Simular High e Low
df['High'] = df[['Open', 'Close']].max(axis=1) * (1 + volatilidade_diaria * np.random.rand(num_candles))
df['Low'] = df[['Open', 'Close']].min(axis=1) * (1 - volatilidade_diaria * np.random.rand(num_candles))
# Ajustar para garantir Low <= Open/Close <= High
df['High'] = np.maximum(df['High'], df[['Open', 'Close']].max(axis=1))
df['Low'] = np.minimum(df['Low'], df[['Open', 'Close']].min(axis=1))


# Simular Volume
df['Volume'] = np.random.randint(1000, 5000, size=num_candles) * (1 + abs(df['Close'] - df['Open']) / df['Open'] * 5)
df['Volume'] = df['Volume'].astype(int)

# Remover a primeira linha que terá NaN no Open devido ao shift, ou preencher
# Para este exemplo, vamos remover a primeira linha para simplificar.
# df.loc[df.index[0], 'Open'] = preco_inicial # Já definido
if num_candles > 0: # Garantir que há dados para processar
    df = df.iloc[1:] # Remove a primeira linha se o Open foi baseado no shift
else:
    # Lidar com o caso de num_candles = 0 ou 1 se necessário
    pass


# 3. Calcular SMA
df[f'SMA{periodo_sma}'] = df['Close'].rolling(window=periodo_sma).mean()

# 4. Calcular Bandas de Bollinger
df['StdDev'] = df['Close'].rolling(window=periodo_sma).std()
df['UpperBand'] = df[f'SMA{periodo_sma}'] + (df['StdDev'] * num_desvios_bollinger)
df['LowerBand'] = df[f'SMA{periodo_sma}'] - (df['StdDev'] * num_desvios_bollinger)

# 5. Calcular RSI
delta = df['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=periodo_rsi).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=periodo_rsi).mean()
# Evitar divisão por zero no RS se loss for 0
rs = gain / loss.replace(0, 0.000001) # Substitui 0 por um valor muito pequeno
df['RSI'] = 100 - (100 / (1 + rs))
# Tratar casos onde loss pode ser 0 e gain > 0 (RSI = 100) ou gain e loss são 0 (RSI = 50 ou indefinido)
df.loc[loss == 0, 'RSI'] = 100 # Se loss é 0 e gain >0, RSI é 100
df.loc[(gain == 0) & (loss == 0), 'RSI'] = 50 # Ou um valor neutro, como 50 ou NaN

# 6. Criar gráfico com Plotly
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    vertical_spacing=0.05,
                    row_heights=[0.6, 0.2, 0.2]) # Alturas relativas para os subplots

# Candlestick
fig.add_trace(go.Candlestick(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             name='Candles'),
              row=1, col=1)

# SMA
fig.add_trace(go.Scatter(x=df.index, y=df[f'SMA{periodo_sma}'],
                         line=dict(color='blue', width=1),
                         name=f'SMA {periodo_sma}'),
              row=1, col=1)

# Bandas de Bollinger
fig.add_trace(go.Scatter(x=df.index, y=df['UpperBand'],
                         line=dict(color='rgba(255,165,0,0.5)', width=1, dash='dash'),
                         name='Upper Bollinger'),
              row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['LowerBand'],
                         line=dict(color='rgba(255,165,0,0.5)', width=1, dash='dash'),
                         fill='tonexty', fillcolor='rgba(255,165,0,0.1)', # Preenche entre Upper e Lower
                         name='Lower Bollinger'),
              row=1, col=1)

# Volume
fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='lightblue'),
              row=2, col=1)

# RSI
fig.add_trace(go.Scatter(x=df.index, y=df['RSI'],
                         line=dict(color='purple', width=1),
                         name='RSI'),
              row=3, col=1)
fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1, opacity=0.5)
fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1, opacity=0.5)

# Layout
fig.update_layout(
    title='Simulador de Mercado com Candlesticks e Indicadores',
    xaxis_title='Data',
    yaxis_title='Preço',
    xaxis_rangeslider_visible=False, # Oculta o range slider padrão do candlestick se preferir
    height=800,
    template='plotly_dark' # Usando um tema escuro
)

fig.update_yaxes(title_text="Volume", row=2, col=1)
fig.update_yaxes(title_text="RSI", row=3, col=1)

fig.show()
```

## Output 3
O `Código 3` gerará um gráfico interativo complexo utilizando Plotly. Este gráfico será dividido em três subplots verticais:

1.  **Primeiro Subplot (Principal):**
    *   **Gráfico de Candlestick:** Exibindo os preços de abertura, máximo, mínimo e fechamento para cada período. Velas verdes (ou de uma cor) indicarão alta e velas vermelhas (ou outra cor) indicarão baixa.
    *   **Média Móvel Simples (SMA):** Uma linha sobreposta aos candles mostrando a tendência de curto/médio prazo.
    *   **Bandas de Bollinger:** Duas linhas (superior e inferior) que formam um canal em torno da SMA, indicando a volatilidade. A área entre as bandas pode ser sombreada.

2.  **Segundo Subplot:**
    *   **Indicador de Volume:** Um gráfico de barras mostrando o volume de negociação para cada candle.

3.  **Terceiro Subplot:**
    *   **Indicador RSI:** Uma linha oscilando entre 0 e 100, com linhas horizontais marcando os níveis de sobrecompra (e.g., 70) e sobrevenda (e.g., 30).

O gráfico será interativo, permitindo:
*   **Zoom:** Aproximar e afastar para ver detalhes ou o panorama geral.
*   **Pan:** Mover o gráfico para visualizar diferentes períodos.
*   **Tooltips:** Ao passar o mouse sobre os candles ou linhas, informações detalhadas (como valores de OHLC, SMA, RSI, Volume) serão exibidas.
*   Opcionalmente, um seletor de intervalo de datas (range slider) pode estar visível abaixo do gráfico principal para facilitar a navegação temporal.

# Geração de Gráficos em Tempo Real

Embora as simulações e gráficos interativos que criamos até agora sejam poderosos para análise histórica ou baseada em dados gerados de uma vez, um passo adiante seria visualizar essas simulações ou dados de mercado (reais ou simulados) atualizando-se em "tempo real" ou em intervalos regulares.

## Introdução ao Dash

Para construir aplicações web analíticas interativas com Python, especialmente aquelas que exigem atualizações dinâmicas ou em tempo real, o framework **Dash** (desenvolvido pela Plotly) é uma excelente escolha.

**O que é Dash?**
*   Dash é um framework Python de código aberto para construir interfaces de usuário analíticas.
*   Ele é construído sobre Flask (um microframework web), Plotly.js (para os gráficos interativos que já usamos) e React.js (uma biblioteca JavaScript para construir interfaces de usuário).
*   Com Dash, você pode escrever aplicações web completas usando apenas Python, sem precisar escrever HTML, CSS ou JavaScript diretamente (embora seja possível customizar com eles).

**Como funciona para "tempo real"?**
*   **Callbacks:** A interatividade em Dash é alcançada através de "callbacks". Callbacks são funções Python que são acionadas automaticamente sempre que uma propriedade de um componente da interface do usuário muda (e.g., um botão é clicado, um valor em um slider é alterado, ou um intervalo de tempo decorre).
*   **Atualização de Gráficos:** Um callback pode ser usado para buscar novos dados (ou gerar novos dados de simulação), reprocessá-los e atualizar as figuras do Plotly exibidas na interface.
*   **Componente dcc.Interval:** Dash possui um componente chamado `dcc.Interval` que pode disparar callbacks em intervalos regulares (e.g., a cada segundo, a cada minuto). Isso permite simular atualizações em "tempo real" para os gráficos, onde os dados são atualizados e o gráfico é redesenhado periodicamente.

**Exemplo de Estrutura (Conceitual):**
1.  **Layout da Aplicação:** Definir a estrutura da página web usando componentes Dash (e.g., `html.Div`, `dcc.Graph`, `dcc.Interval`).
2.  **Função de Geração/Atualização de Dados:** Uma função Python que gera novos dados de candle (como no `Código 3`) ou busca dados de uma fonte.
3.  **Callback:**
    *   **Input:** O componente `dcc.Interval` (para disparar a atualização periodicamente).
    *   **Output:** A propriedade `figure` do componente `dcc.Graph` (onde o gráfico de candlestick é exibido).
    *   **Lógica:** Dentro do callback, chamar a função de geração/atualização de dados e retornar a nova figura do Plotly.

Este tópico estabelece a base para uma futura expansão do projeto, onde as simulações de mercado poderiam evoluir de análises estáticas ou interativas sob demanda para dashboards dinâmicos que refletem mudanças ao longo do tempo.
