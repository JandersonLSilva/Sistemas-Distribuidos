# ---- FUNÇÕES USADAS NA COMUNICAÇÃO ---- #

def send_message(sock, message):
    """
    Função para o envio de mensagens pelo socket
    Converte o dicionário para uma string JSON, depois para bytes e envia a mensagem 
    com um cabeçalho de tamanho para poder enviar dados que são muitos grandes.

    Keywords arguments:
      sock -- socket de comunicação
      message_dict -- mensagem que irá ser enviado
    Returns:
      data[list]: lista com os dados de cada fatia
    """
    # 
    message_bytes = json.dumps(message).encode('utf-8')

    # Converte o tamanho para 4 bytes e define a ordem dos bytes
    header = len(message_bytes).to_bytes(4, byteorder='big')
    
    sock.sendall(header)
    sock.sendall(message_bytes)

def receive_message(sock):
    """
    Recebe uma mensagem com cabeçalho de tamanho e a retorna.

    Keywords arguments:
      sock -- socket de comunicação
    Returns:
      data[list]: lista com os dados de cada fatia
    """
    # Primeiro lê o cabeçalho de 4 bytes
    header_data = sock.recv(4)
    if not header_data:
      return None
    
    # Converte os 4 bytes de volta para um inteiro
    message_length = int.from_bytes(header_data, byteorder='big')
    
    # Lê até todos os dados tiverem sido recebidos e passados para 'received_data'
    received_data = b''
    while len(received_data) < message_length:
      chunk = sock.recv(min(message_length - len(received_data), 4096))
      if not chunk:
        raise ConnectionError("Conexão perdida ao receber dados da mensagem.")
      received_data += chunk
      
    return json.loads(received_data.decode('utf-8'))


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

      # Recebendo os dados json
      chunk = receive_message(client_socket)
      print(f"Resolvendo a fatia de dados: {chunk}")
      
      results = []
      if chunk["task_type"] == 'perfects':
        for value in chunk['payload']:
          results.append(check_perfect_number(value))

      elif chunk['task_type'] == 'friendly':
        for value in chunk['payload']:
          results.append(check_friends_numbers(value[0], value[1]))

      print(f"Enviando resultados: {results}")
      chunk["payload"] = results

      send_message(client_socket, chunk)
      
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
