import time
import os
import clima
import circuito

# Função para limpar a tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Título do jogo
def titulo():
    print('=== Fórmula 26 🧙 ===')

# Rodada
rodada = 5

# Clima
clim = clima.clima

# Circuito
circuit = circuito.circuito[rodada][0]
bandeira = circuito.circuito[rodada][1]
tipo = circuito.circuito[rodada][2]

# Apresenta a rodada
def apresentar_rodada():
    print(f'Rodada: {rodada}/24     {bandeira} {circuit}     {clim}     Circuíto {tipo}')

# Função para apresentar o jogo
def apresentacao():
    luzes = 0
    while luzes < 1:
        limpar_tela()
        titulo()
        apresentar_rodada()
        print('A corrida está prestes a começar!')
        time.sleep(5)
        luzes += 1
    while luzes < 6:
        limpar_tela()
        titulo()
        apresentar_rodada()
        print('A corrida está prestes a começar!')
        print('🔴' * luzes + '⚪' * (5 - luzes))
        time.sleep(1)
        luzes += 1
