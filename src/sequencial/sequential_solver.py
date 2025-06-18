import math

def getDivisorSum(n):
    half = math.floor(n / 2)
    sum = 0
    for i in reversed(range(1, half + 1)):
        if n % i == 0:
            sum += i
            
    return sum

nums = [3, 6, 8, 254, 24, 496, 8128, 444, 234, 678, 999]

for num in nums:
    divisorSum = getDivisorSum(num)
    isPerfect = divisorSum == num
    
    print(f"Número {num} é {"PERFEITO" if isPerfect else "imperfeito"} pois a soma dos divisores dá: {divisorSum}")

