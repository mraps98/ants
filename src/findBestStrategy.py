# find best strategy
scores = []
f = open("./ants.log", "r")
scores.append(f.readline().split(",")[1])
f.close()
highestScore = max(scores)
bestStrategy = scores.index(highestScore)
print("Best Strategy = ", bestStrategy)

# update best strategy in action.dat
f = open("./action.dat", "w")
f.write(bestStrategy)
f.close()