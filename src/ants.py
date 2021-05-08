# ants.py
# This is a module which simulates foraging ants. It is inspired by the
# Ant-Foraging netlogo model
import math
import random
import copy

class Ant:
    """
    This is our virtual ant class. It creates an ant which will work
    to bring food to its nest.
    """

    def __init__(self, patches, x, y, nestid=0, heading=0):
        self.x = x
        self.y = y
        self.carryingFood=False
        self.dropSize = [60, 60]
        self.heading = heading
        self.patches = patches
        self.alive = True
        self.nestid = nestid


    def forward(self, d):
        """
        Move forward along heading.
        """

        theta = math.radians(self.heading)
        dx = d * math.cos(theta)
        dy = d * math.sin(theta)

        self.x += dx
        self.y += dy


    def backward(self, d):
        """
        Move backward along heading.
        """

        forward(-d)


    def left(self, a):
        """
        Rotate left by angle a.
        """

        self.heading -= a


    def right(self, a):
        """
        Rotate right by angle a.
        """

        self.heading += a


    def emitScent(self, scent):
        """
        Emit scent to the current patch
        """
        self.p.chemical[scent] += self.dropSize[scent]
        self.dropSize[scent] -= 5

        if self.dropSize[scent] < 1:
            self.dropSize[scent] = 1


    def pickupFood(self):
        """
        Pick Up Food
        """

        # make sure there is food!
        if self.p.food == 0:
            return

        self.p.food -= 1
        self.carryingFood = True


    def dropFood(self):
        """
        Drop Food
        """
        if not self.carryingFood:
            return
        
        #drop the food
        self.carryingFood = False

        if self.p.nest[self.nestid]:
            self.patches.nestScore[self.nestid] += 1
        else:
            self.p.food += 1


    def wiggle(self):
        """
        Wiggle, as ants are likely to do.
        """
        self.right(random.random() * 40 - random.random() *40)

        while not self.ahead(0).canMove: 
            self.right(10)


    def ahead(self, angle):
        """
        Get the patch that is 1 ahead of our position along the
        given angle.
        """

        theta = math.radians(self.heading + angle)
        x = self.x + math.cos(theta)
        y = self.y + math.sin(theta)

        return self.patches.get(x, y)


    def go(self):
        """
        update one tick's worth of the ant's life
        """
        if not self.alive:
            # dead ants scurry no more
            return

        # get the ant's patch, ahead patch, ahead left, and ahead right
        self.p = self.patches.get(self.x, self.y)
        self.aheadp = self.ahead(0)
        self.leftp = self.ahead(-45)
        self.rightp = self.ahead(45)

        # check to see if we went to the danger zone
        endangered = self.p.danger

        # be the best ant we know how to be
        self.strategy()

        # but we may still die
        if endangered:
            if random.random() < 0.5:
                self.alive = False

        # refresh our scent glands
        for i in range(2):
            self.dropSize[i] += 1.5
            if self.dropSize[i] > 60:
                self.dropSize[i] = 60



    def strategy(self):
        """
        This runs one frame worth of the ant's animation. To change the behavior
        of the ant, override this function.
        """

        if self.p.danger:
            self.emitScent(1)
        
        if self.carryingFood:
            self.returnToNest()
        else:
            self.lookForFood()
    

    def returnToNest(self):
        """
        This is the return to nest strategy. 
        """

        # if we are at our nest, we drop the food and head out
        if self.p.nest[self.nestid]:
            self.dropFood()
            self.right(180)
            self.forward(1)
        else:
            # drop some chemical, this depletes our reserves
            self.emitScent(0)
            self.uphillNestScent() # head toward strongest nest scent
            self.wiggle()          # which is toward the nest
            self.forward(1)


    def lookForFood(self):
        """
        Search for food on the patches.
        """

        if self.p.food > 0:
            # pick up the food
            self.pickupFood()
            self.right(180)
            return
        
        if self.p.chemical[0] > 2:
            self.forward(1)
        elif self.p.chemical[0] < 0.05:
            self.wiggle()
            self.forward(1)
        else:
            self.uphillChemical()
            self.forward(1)


    def uphillChemical(self):
        """
        Move toward strongest chemical smell.
        """

        self.wiggle()

        #sniff ahead, left, and right
        ahead = self.aheadp.chemical[0]
        left = self.leftp.chemical[0]
        right = self.rightp.chemical[0]

        #turn as needed
        if left > ahead or right > ahead:
            if right > left:
                self.right(45)
            else:
                self.left(45)


    def uphillNestScent(self):
        """
        Move toward strongest nest scent
        """
        self.wiggle()

        #sniff ahead, left, and right
        ahead = self.aheadp.nestScent[self.nestid]
        left = self.leftp.nestScent[self.nestid]
        right = self.rightp.nestScent[self.nestid]

        #turn as needed
        if left > ahead or right > ahead:
            if right > left:
                self.right(45)
            else:
                self.left(45)



class Patch:
    """
    This class represents a patch of ground in the ant's world.
    """
    def __init__(self):
        self.chemical = [0, 0]
        self.chemicalSource = [False, False]
        self.food = 0
        self.danger = False
        self.nest = [False, False]
        self.nestScent = [0, 0]
        self.canMove = True
        self.evap = 5

    def go(self):
        for i in range(2):
            self.chemical[i] = (self.chemical[i] *(100-self.evap)/100) # slowly evaporate
            if self.chemical[i] < 0.0001:
                self.chemical[i] = 0
                self.chemicalSource[i] = False

        #clear scents for barriers
        if not self.canMove:
            self.nestScent = [0, 0]
            self.chemical = [0, 0]
            self.chemicalSource = [False, False]
            self.nest = [False, False]
        
        #handle nest scents
        if self.nest[0]:
            self.nestScent[0] = 1000
        else:
            self.nestScent[0] *= 0.99
        if self.nest[1]:
            self.nestScent[1] = 1000
        else:
            self.nestScent[1] *= 0.99


class PatchGrid:
    """
    This is the grid for my patches.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.diffuseRate = 50
        self.nestScore = [0, 0]

        #create the impassible patch
        self.impassible = Patch()
        self.impassible.chemical = [-math.inf, -math.inf]
        self.impassible.nestScent = [-math.inf, -math.inf]
        self.impassible.canMove = False

        #clear the world
        self.clear()
    
    def clear(self):
        """
        Restore the grid to pure blankness.
        """
        self.grid = []

        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                self.grid[i].append(Patch())


    def neighbors(self, y, x):
        """
        Return a list of neighbors 
        """

        miny = max(0, y-1)
        maxy = min(self.height-1, y+1)
        minx = max(0, x-1)
        maxx = min(self.width-1, x+1)

        neighbors = []
        for i in range(miny, maxy+1):
            for j in range(minx, maxx+1):
                if i != y or j != x: 
                    neighbors.append((i, j))

        return neighbors
    

    def diffuse(self, field, srcField):
        """
        Diffuse the given field among its neighbors
        """
        #work out the new values
        result = [[[0, 0] for x in range(self.width)] for y in range(self.height)] 
        for i in range(0, self.height):
            for j in range(0, self.width):
                val = getattr(self.grid[i][j], field)
                for k in range(2):
                    if val[k] == 0: continue

                    for n in self.neighbors(i,j):
                        result[n[0]][n[1]][k] += self.diffuseRate * val[k]/800
                
        
        # set the new values
        for i in range(0, self.height):
            for j in range(0, self.width):
                sf = getattr(self.grid[i][j], srcField)
                vf = getattr(self.grid[i][j], field)
                for k in range(2):
                    if not sf[k]:
                        vf[k] = result[i][j][k]


    def get(self, x, y):
        """
        Returns the patch at coordinate x, y
        """

        # get the grid square we are on
        x = int(round(x))
        y = int(round(y))

        # pass around the impassible
        if x<0 or y<0 or x >= self.width or y >= self.height:
            return self.impassible
        
        # return the requested patch
        return self.grid[y][x]

    def go(self):
        """
        Update all the patches.
        """

        # diffuse fields
        self.diffuse("chemical", "chemicalSource")
        self.diffuse("nestScent", "nest")

        # update the patches
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j].go()


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

        for i in range(count):
            self.ants.append(Ant(self.patches, x, y, nestid))
