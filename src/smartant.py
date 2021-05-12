# smartant.py

from sys import path
from ants import Ant
from patch import Patch
import random


class SmartAnt(Ant):
    def __init__(self, patches, x, y, nestid=0, heading=0):
        super().__init__(patches, x, y, nestid=nestid, heading=heading)
        self.generateRandomString()
        self.actionString = 0  # by default the ants will look for food
        self.score = 0

    def generateRandomString(self):
        self.strategyString = bin(random.getrandbits(262144))

    # action is left right forward wiggle
    #           3     2     1       0
    def generateActionString(self):
        if self.aheadp.danger:
            self.actionString = 1
        elif self.leftp.danger:
            self.actionString = random.randint(4, 7)
        elif self.rightp.danger:
            self.actionString = random.randint(8, 11)
        elif self.aheadp.food:
            self.actionString = 2
        elif self.rightp.food:
            self.actionString = 6
        elif self.leftp.food:
            self.actionString = 10

    def strategy(self):
        """
        A smarter strategy function
        """
        self.generateActionString()


        # read action string from strategy.txt
        self.readActionFromFile()

        if self.p.food:
            self.pickupFood()
        elif self.carryingFood:
            self.returnToNest()
        elif self.p.nest[self.nestid] and self.carryingFood:
                self.dropFood()
                self.score += 1
        elif self.strategyString:
            # self.actionString = ((1 << 4) - 1) & int(self.strategyString, 2)
            if self.actionString == 0:
                self.lookForFood()
            elif self.actionString == 1:
                self.wiggle()
                self.lookForFood()
            elif self.actionString == 2:
                self.forward(1)
                self.lookForFood()
            elif self.actionString == 3:
                self.forward(1)
                self.wiggle()
                self.lookForFood()
            elif self.actionString == 4:
                self.right(45)
                self.lookForFood()
            elif self.actionString == 5:
                self.right(45)
                self.wiggle()
                self.lookForFood()
            elif self.actionString == 6:
                self.right(45)
                self.forward(1)
                self.lookForFood()
            elif self.actionString == 7:
                self.right(45)
                self.forward(1)
                self.wiggle()
                self.lookForFood()
            elif self.actionString == 8:
                self.left(45)
                self.lookForFood()
            elif self.actionString == 9:
                self.left(45)
                self.wiggle()
                self.lookForFood()
            elif self.actionString == 10:
                self.left(45)
                self.forward(1)
                self.lookForFood()
            elif self.actionString == 11:
                self.left(45)
                self.forward(1)
                self.wiggle()
                self.lookForFood()
            elif self.actionString == 12:
                self.left(45)
                self.right(45)
                self.lookForFood()
            elif self.actionString == 13:
                self.left(45)
                self.right(45)
                self.wiggle()
                self.lookForFood()
            elif self.actionString == 14:
                self.left(45)
                self.right(45)
                self.forward(1)
                self.lookForFood()
            elif self.actionString == 15:
                self.left(45)
                self.right(45)
                self.forward(1)
                self.wiggle()
                self.lookForFood()
        else:
            self.lookForFood()

    def printStrategyToFile(self, filename):
        file = open(filename, "a+")
        file.write(self.strategyString + "\n")
        file.close()

    def readStrategyFromFile(self, filename):
        file = open(filename, "r")
        self.strategyString = random.choice(file.read().splitlines())
        file.close()

    def readActionFromFile(self, fileName="./action.dat"):
        file = open(fileName, "r")
        self.actionString = int(file.read())
        file.close()
