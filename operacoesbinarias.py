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