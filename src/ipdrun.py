# ipdrun.py
# run the iterated prisoner's dilemma GA
from ipdga import IPDGA

ga = IPDGA()
print("Population\tMin\tMax")
while True:
    ga.evolve(10)
    ga.tournament()
    scores = []
    for p in ga.p:
        scores.append(p.score)
    scores.sort()
    print(ga.popScore, scores[0], scores[-1], sep="\t")
