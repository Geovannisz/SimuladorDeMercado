import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import random
import numpy as np

# Definindo os parâmetros iniciais
tick_count = 0  # Contador de ticks para cada candle
candle_count = 0  # Contador de candles
current_open = 100  # Inicializado com um valor arbitrário
current_high = current_open
current_low = current_open
current_close = current_open
width = 0.8

# Configurando a figura e os eixos no formato paisagem 16:9
fig, ax = plt.subplots(figsize=(16, 9))
x_window = 80  # Define a largura da janela no eixo x para 80 candles
ax.set_xlim(0, x_window)
ax.set_xlabel('Step')
ax.set_ylabel('Position')

candles = []  # Lista para armazenar os candles
tick_line = None  # Linha que acompanha o valor do tick
current_candle_bar = None  # Barra do candle atual
sma_lines = []  # Lista para armazenar as linhas da média móvel simples
sma_values = []  # Lista para armazenar os valores da média móvel
bollinger_upper_line = None  # Linha da banda superior de Bollinger
bollinger_lower_line = None  # Linha da banda inferior de Bollinger
periods = 20  # Períodos para a média móvel e bandas de Bollinger

# Variáveis de controle para os botões
paused = False
show_sma = True
show_bollinger = True

# Margem para o eixo y
y_margin = 0.01

# Número de ticks por candle
ticks_per_candle = 10

# Inicializando o plot
def init():
    ax.set_xlim(0, x_window)
    ax.set_ylim(95, 105)  # Definindo o eixo vertical inicial entre 95 e 105
    return ax,

# Função para calcular a média móvel simples
def calculate_sma(candles, periods):
    if len(candles) < periods:
        return None  # Não há candles suficientes para calcular a média móvel
    return sum(candle['close'] for candle in candles[-periods:]) / periods

# Função para calcular as bandas de Bollinger
def calculate_bollinger_bands(candles, periods):
    if len(candles) < periods:
        return None, None  # Não há candles suficientes para calcular as bandas
    closes = [candle['close'] for candle in candles[-periods:]]
    sma = calculate_sma(candles, periods)
    std_dev = np.std(closes)
    upper_band = sma + (2 * std_dev)
    lower_band = sma - (2 * std_dev)
    return upper_band, lower_band

# Função para desenhar as bandas de Bollinger
def draw_bollinger_bands(candles, periods):
    global bollinger_upper_line, bollinger_lower_line, dark_mode
    upper_bands, lower_bands = [], []

    if dark_mode:
        cor = 'white'
    else:
        cor = 'black'

    for i in range(periods - 1, len(candles)):
        upper_band, lower_band = calculate_bollinger_bands(candles[:i+1], periods)
        upper_bands.append(upper_band)
        lower_bands.append(lower_band)

    if bollinger_upper_line:
        bollinger_upper_line.remove()
    if bollinger_lower_line:
        bollinger_lower_line.remove()

    bollinger_upper_line = ax.plot(range(periods - 1, len(candles)), upper_bands, 'k--', linewidth=1, alpha=0.75, color=cor)[0]
    bollinger_lower_line = ax.plot(range(periods - 1, len(candles)), lower_bands, 'k--', linewidth=1, alpha=0.75, color=cor)[0]

    # Novo código para lidar com a visibilidade
    bollinger_upper_line.set_visible(show_bollinger)
    bollinger_lower_line.set_visible(show_bollinger)

# Função para desenhar a média móvel simples
def draw_sma(candles, periods):
    global sma_lines, sma_values
    if len(candles) < periods:
        return  # Não há candles suficientes para calcular a média móvel

    # Calculando todos os valores da SMA a partir do vigésimo candle
    sma_values = [calculate_sma(candles[:i+1], periods) for i in range(periods - 1, len(candles))]

    # Removendo as linhas antigas da SMA
    for line in sma_lines:
        line.remove()
    sma_lines.clear()

    # Desenhando as linhas da SMA com a cor apropriada
    for i in range(1, len(sma_values)):
        color = 'green' if sma_values[i] >= sma_values[i-1] else 'red'
        # Ajuste para alinhar o índice do plot da SMA com o índice do candle
        sma_lines.append(ax.plot([i + periods - 1, i + periods], [sma_values[i-1], sma_values[i]], color=color, linewidth=2, alpha=0.7)[0])

    # Novo código para lidar com a visibilidade
    for line in sma_lines:
        line.set_visible(show_sma)

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

# Variável de controle para o modo escuro
dark_mode = False

# Função de callback para alterar para o modo escuro e inverter a paleta de cores
def toggle_dark_mode(event):
    global fig, ax, dark_mode, candles, bollinger_upper_line, bollinger_lower_line
    dark_mode = not dark_mode

    new_color = 'black' if dark_mode else 'white'
    text_color = 'white' if dark_mode else 'black'
    line_color = 'white' if dark_mode else 'black'

    # Atualizar as cores de fundo
    fig.set_facecolor(new_color)
    ax.set_facecolor(new_color)

    # Inverter as cores do texto nos eixos
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    ax.tick_params(axis='x', colors=text_color)
    ax.tick_params(axis='y', colors=text_color)

    # Inverter as cores dos candles, linhas SMA e Bollinger
    for candle in candles:
        draw_candle(candle, redraw=False)  # Redesenhar cada candle com as novas cores
    if candle_count >= periods:
        draw_sma(candles, periods)
        draw_bollinger_bands(candles, periods)

    # Inverter as cores das linhas das bandas de Bollinger
    if bollinger_upper_line:
        bollinger_upper_line.set_color(line_color)
    if bollinger_lower_line:
        bollinger_lower_line.set_color(line_color)

    # Inverter as cores das bordas do gráfico (spines)
    for spine in ax.spines.values():
        spine.set_edgecolor(line_color)

    plt.draw()

# Função para desenhar um candle
def draw_candle(candle, zorder=3, redraw=True):
    global dark_mode
    if dark_mode:
        color = 'green' if candle['close'] >= candle['open'] else 'red'
        edgecolor = 'white'
    else:
        color = 'white' if candle['close'] >= candle['open'] else 'black'
        edgecolor = 'black'

    # Remover o candle anterior se estiver no modo de redesenho
    if redraw and 'bar' in candle:
        for bar in candle['bar']:
            bar.remove()

    bottom = min(candle['open'], candle['close'])
    # Atualizar o candle com as novas cores
    candle['bar'] = ax.bar(candle['index'] + width/2, abs(candle['close'] - candle['open']), bottom=bottom, width=width, color=color, edgecolor=edgecolor, zorder=zorder)
    ax.plot([candle['index'] + width/2, candle['index'] + width/2], [candle['low'], candle['high']], color=edgecolor, zorder=zorder-1)  # Mechas

# Função de callback para pausar/continuar a animação
def toggle_animation(event):
    global paused
    paused = not paused

# Função de callback para mostrar/esconder a média móvel simples
def toggle_sma(event):
    global show_sma
    show_sma = not show_sma
    for line in sma_lines:
        line.set_visible(show_sma)
    plt.draw()

# Função de callback para mostrar/esconder as bandas de Bollinger
def toggle_bollinger(event):
    global show_bollinger
    show_bollinger = not show_bollinger
    bollinger_upper_line.set_visible(show_bollinger)
    bollinger_lower_line.set_visible(show_bollinger)
    plt.draw()

# Função de callback para alterar a cor de fundo do gráfico
def toggle_background_color(event):
    global fig, ax
    color = fig.get_facecolor()
    new_color = 'black' if color == (1.0, 1.0, 1.0, 1.0) else 'white'
    fig.set_facecolor(new_color)
    ax.set_facecolor(new_color)
    plt.draw()

# Função de manipulação de eventos de rolagem do mouse para zoom
def on_scroll(event):
    global x_window
    base_scale = 1.1
    if event.button == 'up':  # Zoom in
        x_window = max(int(x_window / base_scale), 10)
    elif event.button == 'down':  # Zoom out
        x_window = min(int(x_window * base_scale), len(candles))

    # Atualizar os limites do eixo x
    ax.set_xlim(candle_count - x_window + width, candle_count + width)
    plt.draw()

# Função de animação chamada em cada tick
def animate(i):
    if paused:  # Se estiver pausada, não faça nada
        return ax,

    global tick_count, current_open, current_high, current_low, current_close, tick_line, current_candle_bar
    # Atualizar o valor da posição com uma variação aleatória
    step = (random.random() * (1 if random.random() < 0.5 else -1)) / 3
    position = current_close + step

    # Atualizar máximas e mínimas do candle atual
    current_high = max(current_high, position)
    current_low = min(current_low, position)
    current_close = position

    # Atualizar o contador de ticks e, se necessário, adicionar novo candle e desenhá-lo
    tick_count += 1
    if tick_count == ticks_per_candle:
        add_candle()
        draw_candle(candles[-1])
        tick_count = 0

        # Desenhar a média móvel simples e as bandas de Bollinger se houver candles suficientes
        if candle_count >= periods:
            draw_sma(candles, periods)
            draw_bollinger_bands(candles, periods)

    # Atualizar a cor e a altura do candle atual
    if current_candle_bar:
        current_candle_bar.remove()

    bottom = min(current_close, current_open)

    if dark_mode:
        color = 'green' if current_close >= current_open else 'red'
        current_candle_bar = ax.bar(candle_count + width/2, abs(current_close - current_open), bottom=bottom, width=width, color=color, edgecolor='white', zorder=4)
    else:
        color = 'white' if current_close >= current_open else 'black'
        current_candle_bar = ax.bar(candle_count + width/2, abs(current_close - current_open), bottom=bottom, width=width, color=color, edgecolor='black', zorder=4)

    # Desenhar e atualizar a linha do tick
    tick_color = 'green' if step >= 0 else 'red'
    if tick_line is not None:
        tick_line.remove()
    tick_line = ax.axhline(y=position, color=tick_color, linewidth=2, alpha=0.7)

    # Movendo o gráfico para a direita conforme os candles avançam
    ax.set_xlim(candle_count - x_window + width, candle_count + width)

    # Ajustar os limites do gráfico no eixo y para acomodar os candles visíveis
    all_lows = [c['low'] for c in candles[-x_window:]] + [current_low]
    all_highs = [c['high'] for c in candles[-x_window:]] + [current_high]
    min_y = min(all_lows)
    max_y = max(all_highs)
    ax.set_ylim(min(min_y - abs(min_y) * y_margin, 99), max(max_y + abs(max_y) * y_margin, 101)) 

    # Atualize para desenhar a SMA e as bandas de Bollinger apenas se estiverem visíveis
    if candle_count >= periods:
        if show_sma:
            draw_sma(candles, periods)
        if show_bollinger:
            draw_bollinger_bands(candles, periods)

    return ax, tick_line

# Adicionando os botões à figura
axpause = plt.axes([0.7, 0.025, 0.1, 0.04])  # Definindo a posição do botão de pausa
axtoggle_sma = plt.axes([0.55, 0.025, 0.1, 0.04])  # Definindo a posição do botão da SMA
axtoggle_bollinger = plt.axes([0.4, 0.025, 0.1, 0.04])  # Definindo a posição do botão das bandas de Bollinger

btn_pause = Button(axpause, 'Pause/Play')
btn_toggle_sma = Button(axtoggle_sma, 'Toggle SMA')
btn_toggle_bollinger = Button(axtoggle_bollinger, 'Toggle Bollinger')

btn_pause.on_clicked(toggle_animation)
btn_toggle_sma.on_clicked(toggle_sma)
btn_toggle_bollinger.on_clicked(toggle_bollinger)

axtoggle_bg = plt.axes([0.25, 0.025, 0.1, 0.04])  # Definindo a posição do botão de alterar para o modo escuro
btn_toggle_bg = Button(axtoggle_bg, 'Dark Mode')
btn_toggle_bg.on_clicked(toggle_dark_mode)

# Criando a animação e fazendo com que continue indefinidamente
ani = animation.FuncAnimation(fig, animate, init_func=init, interval=0.1, blit=False)

# Conectar a função de rolagem do mouse ao evento de rolagem
fig.canvas.mpl_connect('scroll_event', on_scroll)

# Mostrar a animação
plt.show()