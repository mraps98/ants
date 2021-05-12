for s in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
do
    echo $s > "./action.dat"
    echo "Trying strategy " $s
    python3 main.py 
done