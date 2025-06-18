import math

def getDivisorSum(n):
    half = math.floor(n / 2)
    sum = 0
    for i in reversed(range(1, half + 1)):
        if n % i == 0:
            sum += i
            
    return sum

def getFriendsNumbers(numsObj):
    friendNumbers = list()
    searchNums = list(numsObj)
    searchNums.pop(0)
    
    for numObj in numsObj:
        if(len(searchNums) <= 0): break
        
        couldFriendsList = list(filter(lambda n: (n['number'] == numObj['divisorSum'] and n != numObj), searchNums))
        couldBeFriend = couldFriendsList[0] if len(couldFriendsList) > 0 else None
        
        if(couldBeFriend is not None and couldBeFriend['divisorSum'] ==  numObj['number']):
            friendNumbers.append([numObj, couldBeFriend])
            searchNums.remove(couldBeFriend)
        
        if(len(searchNums) > 0): searchNums.pop(0)
    
    return friendNumbers
        
nums = [3, 6, 8, 254, 24, 496, 8128, 444, 234, 678, 999, 220, 284]
numsObj =  list(map(lambda n: {'number': n, 'divisorSum': getDivisorSum(n)}, nums))

for numObj in numsObj:
    isPerfect = numObj['number'] == numObj['divisorSum']
    
    print(f"Número {numObj['number']} é {"PERFEITO" if isPerfect else "imperfeito"} pois a soma dos divisores dá: {numObj['divisorSum']}")
    
friendNumbers = getFriendsNumbers(numsObj)

if(len(friendNumbers) == 0): print("\nNenhum número é amigo.")

for friends in friendNumbers:
    print(f"Os numeros {list(map(lambda f: f['number'], friends))} são amigos.")
