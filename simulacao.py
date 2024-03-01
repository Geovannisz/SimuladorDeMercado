import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Definindo os parâmetros iniciais
position = 0
opens = [position]
closes = [position]
lows = [position]
highs = [position]
width = 0.8

# Configurando a figura e os eixos no formato paisagem 16:9
fig, ax = plt.subplots(figsize=(16, 9))
x_window = 80  # Define a largura da janela no eixo x
ax.set_xlim(0, x_window)
ax.set_xlabel('Step')
ax.set_ylabel('Position')

# Inicializando o plot
def init():
    ax.set_xlim(0, x_window)
    return ax,

# Função de animação chamada em cada frame
def animate(i):
    global position, opens, closes, lows, highs
    # A partícula move uma distância aleatória entre 0 e 1 para cima ou para baixo
    step = random.random() * (1 if random.random() < 0.5 else -1)
    new_position = position + step
    opens.append(position)
    closes.append(new_position)
    lows.append(min(position, new_position))
    highs.append(max(position, new_position))
    position = new_position
    
    # Desenhar os candles
    while len(ax.patches) > x_window:
        ax.patches[0].remove()
    while len(ax.lines) > x_window * 2:
        ax.lines[0].remove()
    color = 'green' if closes[-1] >= opens[-1] else 'red'
    ax.plot([i, i], [lows[-1], highs[-1]], color='black')  # Mecha
    ax.bar(i, closes[-1] - opens[-1], bottom=min(opens[-1], closes[-1]), width=width, color=color, zorder=3)  # Candle
    
    # Movendo o gráfico para a direita conforme a partícula avança
    if i >= x_window:
        ax.set_xlim(i - x_window + width/2, i + width/2)

    # Ajustar os limites do gráfico no eixo y para acomodar os candles visíveis
    visible_lows = lows[-x_window:]
    visible_highs = highs[-x_window:]
    min_y = min(visible_lows)
    max_y = max(visible_highs)
    ax.set_ylim(min_y - abs(min_y) * 0.1, max_y + abs(max_y) * 0.1)  # Adiciona uma margem de 10%
    
    return ax,

# Criando a animação e fazendo com que continue indefinidamente
ani = animation.FuncAnimation(fig, animate, init_func=init, interval=100, blit=False)

# Mostrar a animação
plt.show()