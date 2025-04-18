def findfactorial(n):
    fact = 1
    for num in range(1, n + 1):
        fact *= num
    print(fact)
n=int(input("enter a number of choice: "))
findfactorial(n)