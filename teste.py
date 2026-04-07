import equipes
import motores

ENGINES = {equipe[0]: motor[3] for equipe in equipes.equipes for motor in motores.motores if equipe[3] == motor[0]}

print(ENGINES)