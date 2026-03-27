import random
import os

def jogo_par_impar():
    while True:
        os.system('clear')
        print("Bem-vindo ao jogo de Par ou Ímpar!")
        
        # Escolha do jogador
        escolha_jogador = input("Escolha Par ou Ímpar (P/I): ").strip().upper()
        while escolha_jogador not in ['P', 'I']:
            escolha_jogador = input("Por favor, escolha P para Par ou I para Ímpar: ").strip().upper()
        
        # Número do jogador
        numero_jogador = int(input("Escolha um número de 1 a 10: "))
        while numero_jogador < 1 or numero_jogador > 10:
            numero_jogador = int(input("Número deve ser entre 1 e 10: "))
        
        # Número do computador
        numero_computador = random.randint(1, 10)
        print(f"O computador escolheu: {numero_computador}")
        
        # Soma
        soma = numero_jogador + numero_computador
        print(f"Soma: {numero_jogador} + {numero_computador} = {soma}")
        
        # Determinar se é par ou ímpar
        if soma % 2 == 0:
            resultado = "Par"
        else:
            resultado = "Ímpar"
        
        print(f"O resultado é: {resultado}")
        
        # Verificar vencedor
        if (escolha_jogador == 'P' and resultado == "Par") or (escolha_jogador == 'I' and resultado == "Ímpar"):
            print("Você venceu!")
        else:
            print("O computador venceu!")
        
        # Perguntar se quer jogar novamente
        jogar_novamente = input("Quer jogar novamente? (S/N): ").strip().upper()
        if jogar_novamente != 'S':
            break

# Executar o jogo
if __name__ == "__main__":
    jogo_par_impar()