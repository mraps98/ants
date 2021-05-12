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

print("Yellow:", sim.patches.nestScore[0], "Red:", sim.patches.nestScore[1])
