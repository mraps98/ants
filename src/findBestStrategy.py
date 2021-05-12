# find best strategy
scores = []
f = open("ants.log", "r")
allLines = f.readlines()

for i in range(1, len(allLines)):
    smartAntScore= allLines[i].split(",")[1]
    scores.append(int(smartAntScore))
f.close()
highestScore = max(scores)
bestStrategy = scores.index(highestScore)
print("Best Strategy = ", bestStrategy)

# update best strategy in action.dat
f = open("./action.dat", "w")
f.write(str(bestStrategy))
f.close()