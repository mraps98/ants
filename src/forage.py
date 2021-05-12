# forage.py
# A simulation of foraging ants
import ants
import simulation
import visualizer

sim = simulation.Simulation(50, 50)
window = visualizer.Visualizer(sim)

for i in range(200):
    sim.go()
    window.update()

print("SmartAnts:", sim.patches.nestScore[0], "NormalAnts:", sim.patches.nestScore[1])


f = open("./ants.log", "a+")
f.writelines(
    "SmartAnts: "
    + str(sim.patches.nestScore[0])
    + " NormalAnts: "
    + str(sim.patches.nestScore[1])
)
f.close()
