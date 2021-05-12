from smartant import SmartAnt
from ants import Ant
from patch import PatchGrid
import random

class Simulation:
    """
    The simulate ant world!
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # construct the patches
        self.patches = PatchGrid(width, height)

        # get ready for ants
        self.ants = []

        # place the nests
        for i in range(2):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            np = self.patches.get(x, y)
            np.nest[i] = True
            np.go()
            self.createAnts(x, y, i, 50)

        # waft that sweet nest scent around
        for i in range(100):
            self.patches.diffuse("nestScent", "nest")
        

        # place two food sources
        for count in range(2):
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)

            self.patches.get(x, y).food = random.randrange(100)
            foodCourt = self.patches.neighbors(y, x)
            for store in foodCourt:
                self.patches.get(store[1], store[0]).food = random.randrange(100)
        
        # place two danger sources
        for count in range(2):
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)

            self.patches.get(x, y).danger = True
            dangerZone = self.patches.neighbors(y, x)
            for area in dangerZone:
                self.patches.get(area[1], area[0]).danger = True

    
    def go(self):
        """
        Run the ants one iteration.
        """

        for a in self.ants:
            a.go()
        
        self.patches.go() 

    def createAnts(self, x, y, nestid, count):
        """
        Create count number of ants.
        Override this function to change the type of ant the simulation creates.
        """

        if nestid == 0:
            for i in range(count):
                self.ants.append(SmartAnt(self.patches, x, y, nestid))
        else:
            for i in range(count):
                self.ants.append(Ant(self.patches, x, y, nestid))
