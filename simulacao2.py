import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Definindo os parâmetros iniciais
tick_count = 0  # Contador de ticks para cada candle
candle_count = 0  # Contador de candles
current_open = 0
current_high = 0
current_low = 0
current_close = 0
width = 0.8

# Configurando a figura e os eixos no formato paisagem 16:9
fig, ax = plt.subplots(figsize=(16, 9))
x_window = 80  # Define a largura da janela no eixo x
ax.set_xlim(0, x_window)
ax.set_xlabel('Step')
ax.set_ylabel('Position')

candles = []  # Lista para armazenar os candles
tick_line = None  # Linha que acompanha o valor do tick
current_candle_bar = None  # Barra do candle atual

# Inicializando o plot
def init():
    ax.set_xlim(0, x_window)
    return ax,

# Função para adicionar um novo candle
def add_candle():
    global candle_count, current_open, current_high, current_low, current_close
    candle = {
        'open': current_open,
        'high': current_high,
        'low': current_low,
        'close': current_close,
        'index': candle_count
    }
    candles.append(candle)
    candle_count += 1
    # Definir a abertura do próximo candle como o fechamento do atual
    current_open = current_close
    current_high = current_close
    current_low = current_close

# Função de animação chamada em cada tick
def animate(i):
    global tick_count, current_open, current_high, current_low, current_close, tick_line, current_candle_bar
    # Atualizar o valor da posição com uma variação aleatória reduzida
    step = (random.random() * (1 if random.random() < 0.5 else -1)) / 3
    position = current_close + step  # A abertura do novo candle é o fechamento do anterior

    # Atualizar máximas e mínimas do candle atual
    current_high = max(current_high, position)
    current_low = min(current_low, position)
    current_close = position

    # Atualizar o contador de ticks e, se necessário, adicionar novo candle
    tick_count += 1
    if tick_count == 10:
        add_candle()
        tick_count = 0

    # Atualizar a cor e a altura do candle atual
    if current_candle_bar:
        current_candle_bar.remove()
    current_candle_bar = ax.bar(candle_count, current_close - current_open, bottom=current_open, width=width, color='grey', zorder=3)

    # Desenhar e atualizar a linha do tick
    tick_color = 'green' if step >= 0 else 'red'
    if tick_line is not None:
        tick_line.remove()
    tick_line = ax.axhline(y=position, color=tick_color, linewidth=2, alpha=0.7)

    # Desenhar os candles anteriores
    for candle in candles:
        color = 'green' if candle['close'] >= candle['open'] else 'red'
        ax.bar(candle['index'], candle['close'] - candle['open'], bottom=min(candle['open'], candle['close']), width=width, color=color, zorder=3)
        ax.plot([candle['index'], candle['index']], [candle['low'], candle['high']], color='black')  # Mechas

    # Movendo o gráfico para a direita conforme os candles avançam
    ax.set_xlim(candle_count - x_window + width/2, candle_count + width/2)

    # Ajustar os limites do gráfico no eixo y para acomodar os candles visíveis
    all_lows = [c['low'] for c in candles] + [current_low]
    all_highs = [c['high'] for c in candles] + [current_high]
    min_y = min(all_lows)
    max_y = max(all_highs)
    ax.set_ylim(min_y - abs(min_y) * 0.1, max_y + abs(max_y) * 0.1)  # Adiciona uma margem de 10%
    
    return ax, tick_line

# Criando a animação e fazendo com que continue indefinidamente
ani = animation.FuncAnimation(fig, animate, init_func=init, interval=100, blit=False)

# Mostrar a animação
plt.show()