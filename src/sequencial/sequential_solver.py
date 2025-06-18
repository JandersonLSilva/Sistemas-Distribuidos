import math
import os

'''  Calcula a soma dos divisores

Entrada: n -> número
Saída: sum -> número
'''
def getDivisorSum(n):
    half = math.floor(n / 2)
    sum = 0
    for i in reversed(range(1, half + 1)):
        if n % i == 0:
            sum += i
            
    return sum

'''  Encontra os números amigos

Entrada: numsObj -> lista[{'number': number, 'divisorSum': number}, ...]
Saída: friendNumbers -> [[number, number], ...] (cada par desses é amigo)
'''
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
  
archive_name = "minimal_test.txt"
file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', archive_name)    
nums = []


# Leitura do arquivo com a lista de números 

with open(file_path, 'r') as arquivo:
    for linha in arquivo:
        numero = int(linha.strip())
        nums.append(numero)


# Cria o objeto com todos os números e a soma dos seus divisores

numsObj =  list(map(lambda n: {'number': n, 'divisorSum': getDivisorSum(n)}, nums))


# Verifica os números perfeitos

for numObj in numsObj:
    isPerfect = numObj['number'] == numObj['divisorSum']
    
    if(isPerfect):
        print(f"Número {numObj['number']} é PERFEITO pois a soma dos divisores dá: {numObj['divisorSum']}")
    

# Calcula quais são os números amigos

friendNumbers = getFriendsNumbers(numsObj)

if(len(friendNumbers) == 0): print("\nNenhum número é amigo.")

for friends in friendNumbers:
    print(f"Os numeros {list(map(lambda f: f['number'], friends))} são amigos.")
