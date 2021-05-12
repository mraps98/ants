# antsga.py

from ga import SimpleGA
from smartant import SmartAnt
from random import random, randrange
from ants import Simulation

class AntsGA(SimpleGA):
    def __init__(self, npop=50):
        self.p = []
        for i in range(npop):
            self.p.append(SmartAnt())

    def tournament(self):
        """
        Run a simulation for 200 steps and set the popScore
        """
        sim = Simulation(50, 50)
        for i in range(200):
            sim.go()

        print("Yellow:", sim.patches.nestScore[0], "Red:", sim.patches.nestScore[1])

        self.popscore = sim.patches.nestScore[0]        

    def select(self):
        """
        Select two parents based on food score
            p = foodScore / popFoodScore
        """
        i = 0
        parents = []

        while len(parents) != 2:
            prob = self.p[i].score / self.p[i].patches.nestScore[self.p[i].nestId]

            if random() <= prob:
                parents.append(self.p[i])

            i = (i+1) % len(self.p)

        return parents[0], parents[1]

    def mate(self, a1, a2):    
        """
        produce two new offspring using a single point of crossover.
        """

        # bitmasks
        m1 = 2**(a1.bits//2) - 1
        m2 = (2**(a1.bits)-1) ^ m1

        # two children
        c1 = SmartAnt()
        c2 = SmartAnt()

        # crossover for c1
        c1.strategy = (a1.strategy & m1) | (a2.strategy & m2)
        c2.strategy = (a1.strategy & m2) | (a2.strategy & m1)

        return (c1, c2)

    def mutate(self, a):
        """
        flip a random bit with probability of 0.0001
        """

        if random() > 0.0001:
            return a

        b = randrange(0, a.bits)
        a.strategyString = a.strategyString ^ (1 << b)

        return a