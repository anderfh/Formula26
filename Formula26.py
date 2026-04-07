#!/usr/bin/env python3

import random
import time
import os
import clima
import equipes
import motores
import mecanicas
import pilotos
import circuito
import apresentacao
import math

# Equipes:
TEAMS = [equipe[0] for equipe in equipes.equipes]

# Motores:
ENGINES = {equipe[0]: motor[3] for equipe in equipes.equipes for motor in motores.motores if equipe[3] == motor[0]}

# Mecânicas:
MECHANICS = {equipe[0]: mecanica[3] for equipe in equipes.equipes for mecanica in mecanicas.mecanicas if equipe[4] == mecanica[0]}

# Aerodinâmica:
AERO = {equipe[0]: equipe[5] for equipe in equipes.equipes}

# Pilotos:
DRIVER = {equipe[0]: piloto[3] for equipe in equipes.equipes for piloto in pilotos.pilotos if equipe[6] == piloto[0]}

# Pista Dominante:
TRACK = {equipe[0]: equipe[7] for equipe in equipes.equipes}

# escolha aleatória do circuito para a corrida
escolha_circuito = circuito.circuito_escolhido

# Tempo de espera entre as rodadas, baseado no número de voltas
SLEEP_BETWEEN_TURNS = math.ceil(500 / escolha_circuito[3])

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

# Função para simular a corrida
def simular_corrida(num_horses=len(TEAMS), max_rounds= escolha_circuito[3]):
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
                if clima.clima in ['☀️']:
                    if sorte < 0.5:
                        if TRACK[TEAMS[i]] in [escolha_circuito[2]]:  # Pista dominante
                            step = 8  # tiro rápido
                            turbo_flags[i] = True
                        else:
                            step = 6
                    elif sorte < 0.8:
                        step = 6
                    else:
                        step = 3
                        pilot_flags[i] = True
                elif clima.clima in ['🌧️']:
                    if sorte < 0.7:
                        step = 6
                    else:
                        step = 3
                        pilot_flags[i] = True
                elif clima.clima in ['⛈️']:
                    if sorte < 0.35:
                        step = 6
                    else:
                        step = 3
                        pilot_flags[i] = True
            horses[i] += step

        limpar_tela()
        apresentacao.titulo()
        apresentacao.apresentar_rodada()
        print(f'Voltas: {round_count}/{max_rounds}')
        imprimir_pista(horses, turbo_flags, pilot_flags)
        # Contagem regressiva do tempo decorrido da rodada
        for elapsed in range(int(SLEEP_BETWEEN_TURNS)):
            time.sleep(1)
            limpar_tela()
            apresentacao.titulo()
            apresentacao.apresentar_rodada()
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
    print('Bem-vindo(a) à Corrida de Fórmula 26!')
    print('''
Regras:
- Cada rodada, os carros avançam de 1 a 6 espaços (com chance de turbo extra).
''')

    num_horses = len(TEAMS)
    print(f'Número de equipes: {num_horses}.')

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
    
    apresentacao.apresentacao()

    winner, final_positions, round_count = simular_corrida(num_horses, max_rounds= escolha_circuito[3])

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
   
    while True:
        novo = input('\nDeseja jogar outra vez? (s/n): ').strip().lower()
        if novo in ('s', 'n'):
            break
        print('Digite s ou n.')

    if novo == 's':
        apresentacao.rodada += 1
        clima.clima = clima.gerar_clima()  # Gera novo clima para a próxima corrida
        circuito.circuito_escolhido = circuito.escolher_circuito()  # Escolhe novo circuito para a próxima corrida
        limpar_tela()
        main()
    else:
        print('Obrigado por jogar! Até a próxima.')

if __name__ == '__main__':
    main()
