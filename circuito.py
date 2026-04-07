import random


circuito = [
    ['teste', 'País', 'Pista', 10],
    ['Melbourne', '🇦🇺', 'M', 58],
    ['Shanghai', '🇨🇳', 'D', 56],
    ['Suzuka', '🇯🇵', 'T', 53],
    ['Sakhir', '🇧🇭', 'D', 57],
    ['Jeddah', '🇸🇦', 'R', 50],
    ['Miami', '🇺🇸', 'M', 57],
    ['Montreal', '🇨🇦', 'U', 70],
    ['Mônaco', '🇲🇨', 'L', 78],
    ['Barcelona', '🇪🇸', 'T', 66],
    ['Red Bull Ring', '🇦🇹', 'M', 71],
    ['Silverstone', '🇬🇧', 'T', 52],
    ['Spa-Francorchamps', '🇧🇪', 'R', 44],
    ['Hungaroring', '🇭🇺', 'D', 70],
    ['Zandvoort', '🇳🇱', 'T', 72],
    ['Monza', '🇮🇹', 'R', 53],
    ['Madrid', '🇪🇸', 'U', 57],
    ['Baku', '🇦🇿', 'U', 51],
    ['Singapura', '🇸🇬', 'L', 62],
    ['COTA', '🇺🇸', 'T', 56],
    ['Cidade do México', '🇲🇽', 'T', 71],
    ['Interlagos', '🇧🇷', 'D', 58],
    ['Las Vegas', '🇺🇸', 'U', 58],
    ['Catar', '🇶🇦', 'M', 57],
    ['Abu Dhabi', '🇦🇪', 'L', 58],
    ['Sochi', '🇷🇺', 'T', 58],
    ['Portimão', '🇵🇹', 'L', 58],
    ['Paul Ricard', '🇫🇷', 'R', 58],
    ]
# 'Urbano', 'Misto', 'Técnico', 'Rápido', 'Lento', 'Desafiador'

# Escolha aleatória do circuito para a corrida
def escolha_circuito():
    circuito_escolhido = random.choice(circuito[1:])  # Ignora a linha de teste
    return circuito_escolhido
circuito_escolhido = escolha_circuito()