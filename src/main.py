from antsga import AntsGA

ga = AntsGA()

while(True):
    ga.evolve(10)
    ga.tournament()
    scores = []
    for p in ga.p:
        scores.append(p.score)
    scores.sort()
    