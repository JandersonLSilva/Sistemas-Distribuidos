# ---- CONFIGURAÇÃO E COMUNICAÇÃO ENTRE O SERVIDOR E CLIENTE VIA SOCKET ---- #
import socket
import json

def client_socket():
  """
  
  """

  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
      client_socket.connect((HOST, PORT))
      print("Cliente conectado ao servidor. Aguardando a fatia a ser resolvida...")

      # Recebendo os dados json codificados e os convertendo para uma lista
      bytes_recv_data = client_socket.recv(4096)
      if not bytes_recv_data:
        print("Não houve envio de dados por parte do servidor. Encerrando.")
        exit()
      
      chunk = json.loads(bytes_recv_data.decode('utf-8'))
      print(f"Resolvendo a fatia de dados: {chunk}")

      results = []
      for value in chunk:
        results.append(check_perfect_number(value))

      print(f"Enviando resultados: {results}")
      bytes_results = json.dumps(results).encode('utf-8')
      client_socket.sendall(bytes_results)
      
      print("Resolução do problema concluído e enviado. Encerrando.")
  except Exception as e:
    print(f"Ocorreu um erro: {e}")


# ---- FUNÇÕES ---- #

def find_divisors(n):
  """
  # Função que encontra os divisores de 'n'
    Começa do 1 e vai até o número 'n'
    Somando os números no vetor 'divisores'
  """
  divisores = []      # vetor para armazenar divisores de 'n'
  for i in range(1, n):
    if n % i == 0:
      divisores.append(i)
  return divisores


def check_perfect_number(n):
  """
  # Função para a verificação de números Perfeitos
    Chama a função 'find_divisors' e soma os números
    Verifica se a soma é igual ou não ao 'n'
  """
  soma = sum(find_divisors(n))
  if soma == n:
    return (n, True)    # número PERFEITO
  else:
    return (n, False)   # número NÃO PERFEITO


def check_friends_numbers(a, b):
  """ 
  # Função para a verificação de números Amigáveis
    Soma os divisores de um número 'a'
    Soma os divisores de um número 'b'
    Compara ambas as somas para ver se são iguais (amigáveis) ou não
  """
  soma_a = sum(find_divisors(a))
  soma_b = sum(find_divisors(b))
  if soma_a == b and soma_b == a:
    ((a, b), True)    # números AMIGÁVEIS
  else:
    ((a, b), False)   # números NÃO AMIGÁVEIS

# ---- BLOCO DE EXECUÇÃO PRINCIPAL DO PROGRAMA ---- #

HOST = '127.0.0.1'
PORT = 50000

client_socket()
