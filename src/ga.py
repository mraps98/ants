class SimpleGA:
    """
    This is an implementation of the basic genetic algorithm.
    It requires a few functions need to be overriden to handle the
    specifics of the problem.
    """

    def __init__(self, p):
        self.p = p


    def nextGen(self):
        """
        Create the next generation. Returns the population.
        """

        p = []
        while len(p) < len(self.p):
            #select mates and produce offspring
            p1, p2 = self.select()
            offspring = self.mate(p1, p2)

            #put the offspring in the next generation (with mutation)
            for child in offspring:
                child=self.mutate(child)
                p.append(child)
            

        # the world belongs to the new generation
        return p


    def evolve(self, generations=10000):
        """
        Let them evolve for generations number of steps.
        """

        for gen in range(generations):
            # run the tournament
            self.tournament()

            # generate the next generation
            self.p = self.nextGen()


    def getPopulation(self):
        """
        Return the current population
        """

        return self.p


    def tournament(self):
        """
        Run the competition, set scores somewhere.
        The default function does nothing, this shoudl be overridden.
        """
        pass


    def select(self):
        """
        Select two members of the population for mating and return
        them.
        The default function just returns the first two elements.
        This should be overridden.
        """

        return self.p[0], self.p[1]


    def mate(self, p1, p2):
        """
        Mate a pair of individuals, and then return how
        they will be represented in the next generation.
        By default, this just returns the parents.
        This should be overridden
        """
        return (p1, p2)


    def mutate(self, child):
        """
        Perform optional mutation on the child.
        The default function just returns the child.
        This should be overriden if you desire mutation.
        """
        return child

            
        
            
