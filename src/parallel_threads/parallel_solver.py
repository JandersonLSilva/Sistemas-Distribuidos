import threading
import os

#################################################################################################################################################
#       FUNÇÕES         #

'''
# Função que encontra os divisores de 'n'
    Começa do 1 e vai até o número 'n'
    Somando os números no vetor 'divisores'
'''
def encontrar_divisores(n):
    divisores = []      # vetor para armazenar divisores de 'n'
    for i in range(1, n): 
        if n % i == 0:
            divisores.append(i)
    return divisores


'''
# Função para a Verificação de números Perfeitos
    Chama a função 'encontrar_divisores' e soma os números
    Verifica se a soma é igual ou não ao 'n'
'''
def verificar_numero_perfeito(n):
    soma = sum(encontrar_divisores(n))
    if soma == n:
        print(f"{n} - número PERFEITO")
    else:
        print(f"{n} - NÃO número Perfeito")


'''
# Funçõa para a Verificação de números Amigáveis
    Soma os divisores de um número 'a'
    Soma os divisores de um número 'b'
    Compara ambas as somas para ver se são iguais (amigáveis) ou não
'''
def verificar_numeros_amigos(a, b):
    soma_a = sum(encontrar_divisores(a))
    soma_b = sum(encontrar_divisores(b))
    if soma_a == b and soma_b == a:
        print(f"{a} e {b} - números AMIGÁVEIS")
    else:
        print(f"{a} e {b} - NÃO números Amigáveis")


# Caminho para o arquivo contendo números para teste
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'minimal_test.txt'))


'''
    Abre o arquivo definido previamente
    Lê as linhas do arquivo
    Remove espaços e quebra de linhas
    Confirma se os valores são digítos mesmo
'''
numeros = []
try:
    with open(file_path, 'r') as arquivo:
        numeros = [int(linha.strip()) for linha in arquivo if linha.strip().isdigit()]
except FileNotFoundError:
    print(f"Arquivo não encontrado em: {file_path}")

#################################################################################################################################################
#       THREADS        #

'''
# Thread para Verificação de números Perfeitos
    Threads feitas para cada número
    Inicia a thread
    Adiciona a nova thread para a lista (vetor)
    Utiliza o 'join' para garantir que todas as threads foram terminadas
'''
threads_n_perfeitos = []
for numero in numeros:
    t = threading.Thread(target=verificar_numero_perfeito, args=(numero,))
    t.start()
    threads_n_perfeitos.append(t)

for t in threads_n_perfeitos:
    t.join()


print("\n===================================")
print("\n Verificação de Números Amigáveis")

'''
# Thread para Verificação de números Amigáveis
    'set' utilizado para o programa não verificar duas vezes os mesmos números
    Loops para definir os números que serão 'a' e 'b' do arquivo definido
    Uma thread para cada par
    Inicia a thread
    Adiciona nova thread a lista (vetor)
    Marca par como verificado
    Utiliza o 'join' para garantir que todas as threads foram terminadas
'''
threads_n_amigaveis = []
verificados = set()

for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        a, b = numeros[i], numeros[j]
        if (a, b) not in verificados and (b, a) not in verificados:
            t = threading.Thread(target=verificar_numeros_amigos, args=(a, b))
            t.start()
            threads_n_amigaveis.append(t)
            verificados.add((a, b))

for t in threads_n_amigaveis:
    t.join()
