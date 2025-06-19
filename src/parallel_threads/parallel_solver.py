import threading
import os

def encontrar_divisores(n):
    divisores = []
    for i in range(1, n):
        if n % i == 0:
            divisores.append(i)
    return divisores

def verificar_numero_perfeito(n):
    soma = sum(encontrar_divisores(n))
    if soma == n:
        print(f"{n} é um número perfeito!")
    else:
        print(f"{n} não é um número perfeito.")

def verificar_numeros_amigos(a, b):
    soma_a = sum(encontrar_divisores(a))
    soma_b = sum(encontrar_divisores(b))
    if soma_a == b and soma_b == a:
        print(f"{a} e {b} são números amigos!")
    else:
        print(f"{a} e {b} não são números amigos.")

# Caminho para o arquivo
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'minimal_test.txt'))

# Lê os números do arquivo
numeros = []
try:
    with open(file_path, 'r') as arquivo:
        numeros = [int(linha.strip()) for linha in arquivo if linha.strip().isdigit()]
except FileNotFoundError:
    print(f"Arquivo não encontrado em: {file_path}")

# Verifica números perfeitos usando threads
threads = []
for numero in numeros:
    t = threading.Thread(target=verificar_numero_perfeito, args=(numero,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("\n--- Verificação de números amigos ---\n")

# Verifica pares de números amigos usando threads
threads = []
verificados = set()

for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        a, b = numeros[i], numeros[j]
        if (a, b) not in verificados and (b, a) not in verificados:
            t = threading.Thread(target=verificar_numeros_amigos, args=(a, b))
            t.start()
            threads.append(t)
            verificados.add((a, b))

for t in threads:
    t.join()
