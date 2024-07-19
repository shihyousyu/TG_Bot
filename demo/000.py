import random

ans = random.randint(1, 100)
l = 1
r = 100

while True:
    n = int(input())
    if n > ans:
        r = n
    
    elif n < ans:
        l = n
    
    else:
        print("you win")
        break
    
    print(f"{l}~{r}")