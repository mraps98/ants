import math
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


