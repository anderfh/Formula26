#!/usr/bin/env python3
"""Jogo simples de corrida de cavalos para terminal (Português)."""

import random
import time
import os

TRACK_LENGTH = None  # Sem limite máximo de posições
SLEEP_BETWEEN_TURNS = 10.0
TEAMS = ['MER', 'FER', 'RED', 'MCL', 'AST', 'ALP', 'WIL', 'HAA', 'AUD', 'RBV', 'CAD', 'APX']

# Motores:
# Mercedes=6 (MER,WIL,MCL), Ferrari=6 (FER,HAA,CAD), Ford=5 (RED,RBV), Honda=3 (AST,ALP), Porsche=4 (AUD,APX)
ENGINES = {'MER':6, 'WIL':6, 'MCL':6, 'FER':6, 'HAA':6, 'CAD':6, 'RED':5, 'RBV':5, 'AST':3, 'ALP':3, 'AUD':4, 'APX':4}
ENGINE_GROUPS = {
    'MER': ['MER', 'WIL', 'MCL'],
    'FER': ['FER', 'HAA', 'CAD'],
    'FOR': ['RED', 'RBV'],
    'HON': ['AST', 'ALP'],
    'POR': ['AUD', 'APX'],
}

# Mecânicas: Mercedes (MER,WIL), McLaren (MCL,APX), Ferrari (FER,CAD), Toyota (HAA), Red Bull (RED,RBV), Aston (AST), Renault (ALP), Audi (AUD)
MECHANICS = {team: 4 for team in TEAMS}
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

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def imprimir_pista(horses, turbo_flags=None, pilot_flags=None):
    # Ordenar por posição decrescente (quem estiver na frente primeiro)
    sorted_horses = sorted(enumerate(horses), key=lambda x: x[1], reverse=True)
    max_pos = sorted_horses[0][1]

    for rank, (idx, pos) in enumerate(sorted_horses, start=1):
        # Primeiro carro fica fixo na frente; os demais recuam de acordo com a diferença.
        diff = max_pos - pos
        visual_diff = min(diff, 20)  # Limite visual para diferenças > 20
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
            if diff >= 60:
                marcador = ' (3v)'
            elif diff >= 40:
                marcador = ' (2v)'
            elif diff >= 20:
                marcador = ' (1v)'
            else:
                marcador = f' (-{diff})'
        print(f'  {rank:>2}. {TEAMS[idx]:>3} {linha}{marcador}')


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
            elif step == 1:
                if random.random() < 0.50:
                    step = 8  # tiro rápido
                    turbo_flags[i] = True
                else:
                    step = 1
                    pilot_flags[i] = True
            horses[i] += step

        limpar_tela()
        print('=== Corrida de Fórmula 1 ===')
        print(f'Rodada: {round_count}/{max_rounds}')
        imprimir_pista(horses, turbo_flags, pilot_flags)
        # Contagem regressiva do tempo decorrido da rodada
        for elapsed in range(int(SLEEP_BETWEEN_TURNS)):
            time.sleep(1)
            limpar_tela()
            print('=== Corrida de Fórmula 1 ===')
            rodada_str = f'Rodada: {round_count}/{max_rounds}'
            tempo_str = f'({elapsed+1:d})'
            # Alinhar relógio a ~40 caracteres da margem esquerda
            espacos = ' ' * max(0, 40 - len(rodada_str))
            print(rodada_str + espacos + tempo_str)
            imprimir_pista(horses, turbo_flags, pilot_flags)

    # Determina o vencedor com base em quem estiver mais à frente na rodada final
    max_pos = max(horses)
    winner = horses.index(max_pos)

    return winner, horses, round_count


def configurar_parametros():
    while True:
        limpar_tela()
        print('=== CONFIGURAÇÃO DE PARÂMETROS ===')
        print('ESCOLHA O TIPO:')
        print('  M - MOTORES')
        print('  E - MECÂNICAS')
        print('  B - VOLTAR')
        tipo = input('> ').strip().upper()
        if tipo == 'B':
            break
        elif tipo == 'M':
            configurar_grupo(ENGINES, ENGINE_GROUPS, 'Motores')
        elif tipo == 'E':
            configurar_grupo(MECHANICS, MECHANIC_GROUPS, 'Mecânicas')
        else:
            print('OPÇÃO INVÁLIDA. PRESSIONE ENTER PARA TENTAR NOVAMENTE.')
            input()


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

    print("\nMENU INICIAL: DIGITE 'J' PARA INICIAR A CORRIDA, 'C' PARA CONFIGURAÇÕES.")
    while True:
        key = input().strip().upper()
        if key == 'J':
            break
        elif key == 'C':
            configurar_parametros()
            limpar_tela()
            print('=== RETORNANDO AO MENU INICIAL ===')
            print("MENU INICIAL: DIGITE 'J' PARA INICIAR A CORRIDA, 'C' PARA CONFIGURAÇÕES.")
        else:
            print("OPÇÃO INVÁLIDA. DIGITE 'J' PARA INICIAR OU 'C' PARA CONFIGURAÇÕES.")

    limpar_tela()
    print('A corrida está prestes a começar!')
    time.sleep(1)

    winner, final_positions, round_count = simular_corrida(num_horses, max_rounds=52)

    # Classificar top 3
    ranked = sorted(enumerate(final_positions), key=lambda x: x[1], reverse=True)
    first = ranked[0][0]
    second = ranked[1][0]
    third = ranked[2][0]

    print(f'\n🏁 Classificação final:')
    print(f'1º lugar: {TEAMS[first]} ({final_positions[first]} posições)')
    print(f'2º lugar: {TEAMS[second]} ({final_positions[second]} posições)')
    print(f'3º lugar: {TEAMS[third]} ({final_positions[third]} posições)')

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
