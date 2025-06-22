# ---- CONFIGURAÇÃO E COMUNICAÇÃO ENTRE O SERVIDOR E CLIENTE VIA SOCKET ---- #
import socket
import json

def client_socket():
  """
  Função que faz a conexão com o servidor e realiza a tarefa passada.
  Cria um socket para conexão e recebe os dados em json decide qual função deverá executar
  e envia os dados verificados de volta para o servidor.
  """

  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
      client_socket.connect((HOST, PORT))
      print("Cliente conectado ao servidor. Aguardando a fatia a ser resolvida...")

      # Recebendo os dados json codificados e os convertendo para uma lista
      bytes_recv_data = client_socket.recv(4096)
      if not bytes_recv_data:
        print("Não houve envio de dados por parte do servidor. Encerrando.")
        exit(1)
      
      chunk = json.loads(bytes_recv_data.decode('utf-8'))
      print(f"Resolvendo a fatia de dados: {chunk}")

      print(chunk)
      
      results = []
      if chunk["task_type"] == 'perfects':
        for value in chunk['payload']:
          results.append(check_perfect_number(value))

      elif chunk['task_type'] == 'friendly':
        for value in chunk['payload']:
          results.append(check_friends_numbers(value[0], value[1]))

      print(f"Enviando resultados: {results}")
      chunk["payload"] = results
      bytes_results = json.dumps(chunk).encode('utf-8')
      client_socket.sendall(bytes_results)
      
      print("Resolução do problema concluído e enviado. Encerrando.")
  except Exception as e:
    print(f"Ocorreu um erro: {e}")


# ---- FUNÇÕES COM AS RESOLUÇÕES DOS PROBLEMAS ---- #

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
  sum_dv = sum(find_divisors(n))
  if sum_dv == n:
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
  sum_a = sum(find_divisors(a))
  sum_b = sum(find_divisors(b))
  if sum_a == b and sum_b == a:
    return ((a, b), True)    # números AMIGÁVEIS
  else:
    return ((a, b), False)   # números NÃO AMIGÁVEIS


# ---- BLOCO DE EXECUÇÃO PRINCIPAL DO PROGRAMA ---- #

HOST = '127.0.0.1'
PORT = 50000

client_socket()
