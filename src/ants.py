# ants.py
# This is a module which simulates foraging ants. It is inspired by the
# Ant-Foraging netlogo model
import math
import random

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