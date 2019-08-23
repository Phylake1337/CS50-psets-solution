from cs50 import get_int

n = get_int("Height: ")

while not (0 < n < 9):
    n = get_int("Height: ")

for i in range(1 , n+1):
    print((n - i) * " " + (i) * "#" + "  " + (i) * "#")