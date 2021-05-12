# forage.py
# A simulation of foraging ants
from typing import DefaultDict
import ants
import simulation
import visualizer

sim = simulation.Simulation(50, 50)

for i in range(200):
    sim.go()

f = open("./action.dat", "r")
currentAction = int(f.read())
f.close()

print(currentAction, sim.patches.nestScore[0], sim.patches.nestScore[1], sep=",")


f = open("./ants.log", "a+")
f.writelines("{},{},{}\n".format(currentAction, sim.patches.nestScore[0], sim.patches.nestScore[1]))
f.close()