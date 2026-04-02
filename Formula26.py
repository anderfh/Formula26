#!/usr/bin/env python3
"""Jogo simples de corrida de cavalos para terminal (Português)."""

import random
import time
import os

TRACK_LENGTH = None  # Sem limite máximo de posições
SLEEP_BETWEEN_TURNS = 10.0
# Equipes:
TEAMS = ['MER', 'FER', 'RED', 'MCL', 'AST', 'ALP', 'WIL', 'HAA', 'AUD', 'RBV', 'CAD', 'APX']

# Motores:
ENGINES = {'MER':6, 'WIL':6, 'MCL':6, 'FER':6, 'HAA':6, 'CAD':6, 'RED':5, 'RBV':5, 'AST':3, 'ALP':3, 'AUD':4, 'APX':4}
ENGINE_GROUPS = {
    'MER': ['MER', 'WIL', 'MCL'],
    'FER': ['FER', 'HAA', 'CAD'],
    'FOR': ['RED', 'RBV'],
    'HON': ['AST', 'ALP'],
    'POR': ['AUD', 'APX'],
}

# Mecânicas:
MECHANICS = {'MER':6, 'WIL':6, 'MCL':6, 'FER':6, 'HAA':5, 'CAD':6, 'RED':5, 'RBV':5, 'AST':4, 'ALP':5, 'AUD':5, 'APX':6}
MECHANIC_GROUPS = {
    'MER': ['MER', 'WIL'],
    'MCL': ['MCL', 'APX'],
    'FER': ['FER', 'CAD'],
    'TOY': ['HAA'],
    'RED': ['RED', 'RBV'],
    'AST': ['AST'],
    'REN': ['ALP'],
    'AUD': ['AUD'],
}

# Aerodinâmica:
AERO = {'MER':6, 'WIL':4, 'MCL':6, 'FER':6, 'HAA':5, 'CAD':4, 'RED':5, 'RBV':5, 'AST':4, 'ALP':5, 'AUD':4, 'APX':4}
AERO_GROUPS = {time: [time] for time in TEAMS}

# Pilotos:
DRIVER = {'MER':6, 'WIL':5, 'MCL':6, 'FER':6, 'HAA':5, 'CAD':5, 'RED':6, 'RBV':4, 'AST':6, 'ALP':5, 'AUD':4, 'APX':4}
DRIVER_GROUPS = {
    'CHAMPION': ['MER', 'MCL', 'FER', 'RED', 'AST'],
    'WINNER': ['WIL', 'HAA', 'ALP', 'CAD'],
    'NONE': ['RBV', 'AUD', 'APX'],
}
# Clima:
def gerar_clima():
    clima = random.choice(['☀️', '☀️', '☀️', '☀️', '🌧️', '⛈️'])
    return clima
clima = gerar_clima()

# Pista Dominante:
def pista_dominante():
    pista = random.choice(['Urbano', 'Misto', 'Técnico', 'Rápido', 'Lento', 'Desafiador'])
    return pista
pista = pista_dominante()

# Pista x Equipes:
TRACK_GROUPS = {
    'Urbano': ['FER', 'HAA'],
    'Misto': ['RED', 'ALP'],
    'Técnico': ['AUD', 'APX'],
    'Rápido': ['MER', 'WIL'],
    'Lento': ['MCL', 'CAD'],
    'Desafiador': ['RBV', 'AST']
}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para imprimir a pista de corrida
def imprimir_pista(horses, turbo_flags=None, pilot_flags=None):
    # Ordenar por posição decrescente (quem estiver na frente primeiro)
    sorted_horses = sorted(enumerate(horses), key=lambda x: x[1], reverse=True)
    max_pos = sorted_horses[0][1]

    for rank, (idx, pos) in enumerate(sorted_horses, start=1):
        # Primeiro carro fica fixo na frente; os demais recuam de acordo com a diferença.
        diff = max_pos - pos
        visual_diff = min(diff, 40)  # Limite visual para diferenças > 40
        ficam = ' ' * visual_diff
        carro = '🏎️   '
        if turbo_flags and turbo_flags[idx]:
            carro = '🏎️ 💨'
        if pilot_flags and pilot_flags[idx]:
            carro = '🏎️  ⚠️'  # Símbolo de aviso
        
        linha = '[ ' + ficam + carro + ' ]'  # barra fixa, espaço extra por diferença
        if rank == 1:
            marcador = ' (Líder)'
        else:
            if diff >= 120:
                marcador = ' (3v)'
            elif diff >= 80:
                marcador = ' (2v)'
            elif diff >= 40:
                marcador = ' (1v)'
            else:
                marcador = f' (-{diff})'
        print(f'  {rank:>2}. {TEAMS[idx]:>3} {linha}{marcador}')

# Função para escolher a aposta do jogador
def escolher_aposta(num_horses):
    print("Equipes disponíveis:")
    for i, team in enumerate(TEAMS):
        print(f"  {i+1}. {team}")
    while True:
        escolha = input("Escolha uma equipe (digite o número): ").strip()
        if not escolha.isdigit():
            print('Por favor digite um número válido.')
            continue
        escolha = int(escolha)
        if 1 <= escolha <= num_horses:
            return escolha - 1
        print(f'Escolha entre 1 e {num_horses}.')

# Função para apresentar o jogo
def apresentacao():
    luzes = 0
    while luzes < 1:
        limpar_tela()
        print('=== Fórmula 26 🧙 ===')
        print('Rodada: 1/24     Melbourne     ' + clima + '     Circuíto ' + pista)
        print('A corrida está prestes a começar!')
        time.sleep(5)
        luzes += 1
    while luzes < 6:
        limpar_tela()
        print('=== Fórmula 26 🧙 ===')
        print('Rodada: 1/24     Melbourne     ' + clima + '     Circuíto ' + pista)
        print('A corrida está prestes a começar!')
        print('🔴' * luzes + '⚪' * (5 - luzes))
        time.sleep(1)
        luzes += 1

# Função para simular a corrida
def simular_corrida(num_horses=5, max_rounds=52):
    horses = [0] * num_horses
    round_count = 0

    while round_count < max_rounds:
        round_count += 1
        turbo_flags = [False] * num_horses
        pilot_flags = [False] * num_horses
        for i in range(num_horses):
            # Avanço aleatório leve: 1 a 6 passos, com chance de pulo extra
            step = random.randint(1, 6)
            if step == 2:
                step = ENGINES[TEAMS[i]]
            elif step == 3:
                step = MECHANICS[TEAMS[i]]
            elif step == 4:
                step = AERO[TEAMS[i]]
            elif step == 5:
                step = DRIVER[TEAMS[i]]
            elif step == 1:
                sorte = random.random()
                if clima in ['☀️']:
                    if sorte < 0.5:
                        if TEAMS[i] in TRACK_GROUPS[pista]:
                            step = 8  # tiro rápido
                            turbo_flags[i] = True
                        else:
                            step = 6
                    elif sorte < 0.8:
                        step = 6
                    else:
                        step = 3
                        pilot_flags[i] = True
                elif clima in ['🌧️']:
                    if sorte < 0.7:
                        step = 6
                    else:
                        step = 3
                        pilot_flags[i] = True
                elif clima in ['⛈️']:
                    if sorte < 0.35:
                        step = 6
                    else:
                        step = 3
                        pilot_flags[i] = True
            horses[i] += step

        limpar_tela()
        print('=== Fórmula 26 🧙 ===')
        print(f'Rodada: 1/24     Melbourne     {clima}     Circuíto {pista}')
        print(f'Voltas: {round_count}/{max_rounds}')
        imprimir_pista(horses, turbo_flags, pilot_flags)
        # Contagem regressiva do tempo decorrido da rodada
        for elapsed in range(int(SLEEP_BETWEEN_TURNS)):
            time.sleep(1)
            limpar_tela()
            print('=== Fórmula 26 🧙 ===')
            print(f'Rodada: 1/24     Melbourne     {clima}     Circuíto {pista}')
            voltas_str = f'Voltas: {round_count}/{max_rounds}'
            tempo_str = f'({elapsed+1:d})'
            # Alinhar relógio a ~60 caracteres da margem esquerda
            espacos = ' ' * max(0, 60 - len(voltas_str))
            print(voltas_str + espacos + tempo_str)
            imprimir_pista(horses, turbo_flags, pilot_flags)

    # Determina o vencedor com base em quem estiver mais à frente na rodada final
    max_pos = max(horses)
    winner = horses.index(max_pos)

    return winner, horses, round_count

# Função para configurar parâmetros de motores, mecânicas, aerodinâmica e pilotos
def configurar_parametros():
    while True:
        limpar_tela()
        print('=== CONFIGURAÇÃO DE PARÂMETROS ===')
        print('ESCOLHA O TIPO:')
        print('  M - MOTORES')
        print('  E - MECÂNICAS')
        print('  A - AERODINÂMICA')
        print('  P - PILOTO')
        print('  B - VOLTAR')
        tipo = input('> ').strip().upper()
        if tipo == 'B':
            break
        elif tipo == 'M':
            configurar_grupo(ENGINES, ENGINE_GROUPS, 'Motores')
        elif tipo == 'E':
            configurar_grupo(MECHANICS, MECHANIC_GROUPS, 'Mecânicas')
        elif tipo == 'A':
            configurar_grupo(AERO, AERO_GROUPS, 'Aerodinâmica')
        elif tipo == 'P':
            configurar_grupo(DRIVER, DRIVER_GROUPS, 'Pilotos')
        else:
            print('OPÇÃO INVÁLIDA. PRESSIONE ENTER PARA TENTAR NOVAMENTE.')
            input()

# Função para configurar grupos de parâmetros (motores, mecânicas, aerodinâmica, pilotos)
def configurar_grupo(param_dict, group_dict, nome):
    while True:
        limpar_tela()
        print(f'=== CONFIGURAÇÃO DE {nome.upper()} ===')
        print('Grupos e valores atuais:')
        for grupo, equipes in group_dict.items():
            valor = param_dict[equipes[0]]
            print(f'  {grupo} ({", ".join(equipes)}): {valor}')
        print(f'\nDigite o código do grupo para ajustar, ou B para voltar.')
        escolha = input('> ').strip().upper()
        if escolha == 'B':
            break
        if escolha not in group_dict:
            print('OPÇÃO INVÁLIDA. PRESSIONE ENTER PARA TENTAR NOVAMENTE.')
            input()
            continue

        while True:
            equipes = group_dict[escolha]
            novo_valor = input(f'Digite novo valor de {nome.lower()} para {escolha} (atual {param_dict[equipes[0]]}): ').strip()
            if not novo_valor.isdigit():
                print('DIGITE UM NÚMERO INTEIRO VÁLIDO.')
                continue
            novo_valor = int(novo_valor)
            for team in equipes:
                param_dict[team] = novo_valor
            print(f'VALORES DE {escolha} ATUALIZADOS PARA {novo_valor}. PRESSIONE ENTER PARA CONTINUAR.')
            input()
            break

# Função principal do jogo
def main():
    limpar_tela()
    print('Bem-vindo(a) à Corrida de Fórmula 1!')
    print('''
Regras:
- Você escolhe uma equipe para apostar.
- Cada rodada, os carros avançam de 1 a 6 espaços (com chance de turbo extra).
- A corrida dura 52 rodadas; o vencedor é quem estiver mais à frente no final.
''')

    num_horses = len(TEAMS)
    print(f'Número de equipes: {num_horses}.')
    aposta = len(TEAMS) - 1  # Sempre aposta em APX (última equipe)
    print(f'Aposta automática na equipe {TEAMS[aposta]}.')

    print("\nMENU INICIAL:")
    print("DIGITE 'J' PARA INICIAR A CORRIDA")
    print("DIGITE 'C' PARA CONFIGURAÇÕES.")
    while True:
        key = input().strip().upper()
        if key == 'J':
            break
        elif key == 'C':
            configurar_parametros()
            limpar_tela()
            main()  # Reinicia o jogo após configuração
        else:
            print("OPÇÃO INVÁLIDA. PRESSIONE ENTER PARA TENTAR NOVAMENTE.")
            input()
            limpar_tela()
            main()

    apresentacao()

    winner, final_positions, round_count = simular_corrida(num_horses, max_rounds=52)

    # Classificar top 6 posições
    ranked = sorted(enumerate(final_positions), key=lambda x: x[1], reverse=True)
    first = ranked[0][0]
    second = ranked[1][0]
    third = ranked[2][0]
    fourth = ranked[3][0]
    fifth = ranked[4][0]
    sixth = ranked[5][0]


    print(f'\n🏁 Classificação final:')
    print(f'1º lugar: {TEAMS[first]} (12 pontos)')
    print(f'2º lugar: {TEAMS[second]} (9 pontos)')
    print(f'3º lugar: {TEAMS[third]} (6 pontos)')
    print(f'4º lugar: {TEAMS[fourth]} (4 pontos)')
    print(f'5º lugar: {TEAMS[fifth]} (2 pontos)')
    print(f'6º lugar: {TEAMS[sixth]} (1 pontos)')
    
    if aposta == first:
        print('\n🎉 Parabéns! Sua aposta ganhou!')
    else:
        print(f'\n😞 Você apostou na equipe {TEAMS[aposta]}. Mais sorte na próxima!')

    while True:
        novo = input('Deseja jogar outra vez? (s/n): ').strip().lower()
        if novo in ('s', 'n'):
            break
        print('Digite s ou n.')

    if novo == 's':
        limpar_tela()
        main()
    else:
        print('Obrigado por jogar! Até a próxima.')


if __name__ == '__main__':
    main()
