rm -f ants.log
echo "Strategy, SmartAntsScore, NormalAntsScore"
echo "Stategy, SmartAntsScore, NormalAntsScore" > ants.log
for s in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
    echo $s > "./action.dat"
    python3 main.py 
done