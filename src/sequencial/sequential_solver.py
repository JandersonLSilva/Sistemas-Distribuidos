import math

def getDivisorSum(n):
    half = math.floor(n / 2)
    sum = 0
    for i in reversed(range(1, half + 1)):
        if n % i == 0:
            sum += i
            
    return sum

def getFriendsNumbers(numsObj):
    nums = []
    
    # retornar um array [[6, 8], [4, 9], [4, 9, 76]]
        

nums = [3, 6, 8, 254, 24, 496, 8128, 444, 234, 678, 999]
numsObj =  map(lambda n: {'number': n, 'divisorSum': getDivisorSum(n)}, nums)

for numObj in numsObj:
    isPerfect = numObj['number'] == numObj['divisorSum']
    
    print(f"Número {numObj['number']} é {"PERFEITO" if isPerfect else "imperfeito"} pois a soma dos divisores dá: {numObj['divisorSum']}")
