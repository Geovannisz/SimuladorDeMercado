import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import pandas as pd

# Parâmetros da simulação
n = 10000  # Número de passos
t = 1/n  # Passo de tempo
mu = 0.5  # Taxa de crescimento
v0 = 0.1  # Volatilidade inicial
kappa = 1  # Parâmetro de reversão à média
theta = 0.05  # Nível de longo prazo da volatilidade
sigma = 0.2  # Volatilidade da volatilidade
periodo = [20, 50, 200] # Periodos das Médias
pe = 14 # Fator do RSI

mostrar_bandas = {
    20: False,
    50: False,
    200: False
}

def g(y, v, t, mu, kappa, theta, sigma, n):
    valor_atual = 1
    f = np.zeros(n)
    v_t = np.zeros(n)
    f[0] = np.log(valor_atual)
    v_t[0] = v
    for i in range(n-1):
        aleatorio_v = np.random.normal(0, sigma)
        aleatorio_x = np.random.normal(0, np.sqrt((v_t[i])**2))
        v_t[i+1] = max(0, v_t[i] + kappa * (theta - v_t[i]) * t + sigma * np.sqrt(t) * aleatorio_v)
        f[i+1] = f[i] + mu * t + v_t[i]**0.5 * aleatorio_x
        valor_atual *= np.exp(f[i+1] - f[i])
    return f, v_t

def media(periodo, f):
    xe = np.arange(0, n, 1)
    med = pd.Series(np.exp(f)).rolling(window=periodo).mean()
    std = pd.Series(np.exp(f)).rolling(window=periodo).std()
    mais = med + 2 * std
    menos = med - 2 * std
    
    # Preenche os valores ausentes com NaN
    med = med.fillna(np.nan)
    std = std.fillna(np.nan)
    mais = mais.fillna(np.nan)
    menos = menos.fillna(np.nan)
    
    return xe, med, std, mais, menos

def rsi(f, pe):
    variacao = np.diff(f)
    ganho = np.where(variacao > 0, variacao, 0)
    perda = np.where(variacao < 0, -variacao, 0)

    avg_ganho = pd.Series(ganho).rolling(window=pe).mean()
    avg_perda = pd.Series(perda).rolling(window=pe).mean()

    rs = avg_ganho / avg_perda
    rsi = 100 - (100 / (1 + rs))
    return rsi

f1, v_t = g(np.random.rand(n), v0, t, mu, kappa, theta, sigma, n)
rsi = rsi(f1, pe)
y30, y70 = [], []
for i in range(len(rsi)):
    y30.append(30)
    y70.append(70)

abertura, fechamento, maximo, minimo, volume = [], [], [], [], []
for m in range(0,n-1):
    ep = np.exp(f1[m+1]) - np.exp(f1[m])
    abertura.append(np.exp(f1[m]))
    fechamento.append(np.exp(f1[m+1]))
    
    if ep >= 0:
        maximo.append(fechamento[m] + np.random.uniform(0, ep))
        minimo.append(abertura[m] - np.random.uniform(0, ep/2))
    else:
        maximo.append(abertura[m] + np.random.uniform(0, abs(ep)/2))
        minimo.append(fechamento[m] - np.random.uniform(0, abs(ep)))
    
    volume.append(maximo[m] - minimo[m])

preco = pd.DataFrame({'open': abertura,
                        'close': fechamento,
                        'high': maximo,
                        'low': minimo},
                        index=pd.date_range("2021-01-01", periods=n-1, freq="d"))

fig = make_subplots(rows=1, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0,
                        row_heights=[3])

fig.add_trace(go.Candlestick(x=pd.date_range("2021-01-01", periods=n-1, freq="d"),
                                open=abertura,
                                high=maximo,
                                low=minimo,
                                close=fechamento,
                                increasing_line_color='black',
                                decreasing_line_color='black',
                                increasing_fillcolor='white',
                                decreasing_fillcolor='black',
                                line=dict(width=0.5),
                                name='Candles'),
                        row=1, col=1)

fig.add_trace(go.Scatter(x=pd.date_range("2021-01-01", periods=n, freq="d"), y=np.exp(f1),
                            mode='lines',
                            line=dict(color='yellow', width=1),
                            name='Linha'),
                        row=1, col=1)

#fig.add_trace(go.Scatter(x=pd.date_range("2021-01-01", periods=len(rsi), freq="d"), y=rsi,
#                            mode='lines',
#                            line=dict(color='white', width=1.5),
#                            name='RSI'),
#                        row=2, col=1)
#fig.add_trace(go.Scatter(x=pd.date_range("2021-01-01", periods=len(rsi), freq="d"), y=y70,
#                            mode='lines',
#                            line=dict(color='green', width=1),
#                            line_dash='dash',
#                            name='RSI 70%'),
#                        row=2, col=1)
#fig.add_trace(go.Scatter(x=pd.date_range("2021-01-01", periods=len(rsi), freq="d"), y=y30,
#                            mode='lines',
#                            line=dict(color='red', width=1),
#                            line_dash='dash',
#                            name='RSI 30%'),
#                        row=2, col=1)
#
#fig.add_trace(go.Bar(x=pd.date_range("2021-01-01", periods=n-1, freq="d"), y=volume,
#                        marker=dict(color='black'),
#                        name='Volume'),
#                        row=2, col=1)

for p in periodo:
    c = np.random.uniform(0.5, 1, 3)
    xe, med, std, mais, menos = media(p, f1)
    
    if mostrar_bandas[p]:
        fig.add_trace(go.Scatter(
            x=pd.date_range("2021-01-01", periods=n, freq="d"),
            y=mais,
            mode='lines',
            line=dict(color=f'rgb({c[0]*255},{c[1]*255},{c[2]*255})'),
            name=f'Superior {p}',
            line_dash='dash',
            line_width=1,
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=pd.date_range("2021-01-01", periods=n, freq="d"),
            y=menos,
            mode='lines',
            line=dict(color=f'rgb({c[0]*255},{c[1]*255},{c[2]*255})'),
            name=f'Inferior {p}',
            line_dash='dash',
            line_width=1,
            showlegend=False
        ))
    
    fig.add_trace(go.Scatter(x=pd.date_range("2021-01-01", periods=n, freq="d"),
                             y=med,
                             mode='lines',
                             line=dict(color=f'rgb({c[0]*255},{c[1]*255},{c[2]*255})'),
                             name=f'Periodo {p}',
                             line_width=2))

fig.update_layout(
    title='Simulação de Heston',
    xaxis=dict(showline=True, linewidth=1, linecolor='black', mirror=True, range=[pd.date_range("2021-01-01", periods=n, freq="d")[0], pd.date_range("2021-01-01", periods=n, freq="d")[-1]]),
    yaxis=dict(title='Saldo (R$)', showline=True, linewidth=1, linecolor='black', mirror=True),
    showlegend=True,
    xaxis_rangeslider_visible=False,
    template="simple_white",
    height=800,
    width=1600,  # Set the width of the graph
    autosize=False,  # Disable autosizing
    margin=dict(l=5, r=5, t=5, b=5),  # Set the margins
)

fig.show()