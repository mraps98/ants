# iantsga.py
from random import randrange, random
from ga import SimpleGA

class IPDGA(SimpleGA):
    def __init__(self, npop=100, r=1):
        # generate the population
        self.p = []
        for i in range(npop):
            self.p.append(Player(r))

        # store the number of rounds
        self.r = r

        # dictionary relating histories vs opponent
        self.history = {}

    def tournament(self):
        popScore = 0
        for i in range(len(self.p)):
            # zero out score for player i
            self.p[i].score = 0
            
            for j in range(len(self.p)):
                # get the history strings
                if not (i, j) in self.history.keys():
                    self.history[(i,j)] = []
                if not (j, i) in self.history.keys():
                    self.history[(j,i)] = []
                me = self.history[(i,j)]
                other = self.history[(j, i)]

                pi = self.p[i].play(me, other)
                pj = self.p[j].play(other, me)
                if pi == 0 and pj == 0:
                    score = 1
                elif pi == 0 and pj == 1:
                    score = 5
                elif pi == 1 and pj == 0:
                    score = 0
                elif pi == 1 and pj == 1:
                    score = 3
                self.p[i].score += score
                popScore += score

                # remember the outcomes
                self.history[(i,j)].append(pi)
                self.history[(j,i)].append(pj)
                if len(self.history[(i,j)])>self.r:
                    self.history[(i,j)].remove(me[0])
                    self.history[(j,i)].remove(other[0])

                # remember the population score
                self.popScore = popScore


    def select(self):
        """
        Select two parents based on relative fitness
            p = score / popScore
        """

        # stating conditions
        i = 0
        parents = []

        while len(parents) != 2:
            # probability of selection of self.p[i]
            prob = self.p[i].score / self.popScore

            # check to see if we select this individual
            if random() <= prob:
                parents.append(self.p[i])

            # go to the next
            i = (i+1) % len(self.p)

        return parents[0], parents[1]


    def mate(self, p1, p2):
        """
        produce two new offspring using a single point of crossover.
        """

        # bitmasks
        m1 = 2**(p1.bits//2) - 1
        m2 = (2**(p1.bits)-1) ^ m1

        # two children
        c1 = Player(self.r)
        c2 = Player(self.r)

        # crossover for c1
        c1.strategy = (p1.strategy & m1) | (p2.strategy & m2)
        c2.strategy = (p1.strategy & m2) | (p2.strategy & m1)

        return (c1, c2)
    

    def mutate(self, p):
        """
        flip a random bit with probability of 0.0001
        """

        if random() > 0.0001:
            return p

        b = randrange(0, p.bits)
        p.strategy = p.strategy ^ (1 << b)

        return p
