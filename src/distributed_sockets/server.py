# ---- LEITURA DO ARQUIVO COM OS DADOS ---- #
from pathlib import Path

def read_data():
  """
  Lê um arquivo com dados de teste e extrai todas as linhas que contém somente números.
  Usa a compressão de lista para filtrar e aplicar uma modificação ao elemento
  O caminho é resolvido de forma relativa.

  Returns:
  list[int]: Uma lista de números inteiros contendo os valores do arquivo
             Retorna uma lista vazia caso o arquivo não seja encontrado
  """

  # Resolução do caminho para o arquivo contendo valores para os testes
  file_path = (Path(__file__).parent / '..' / '..' / 'data' / data_file).resolve()

  try:
    with open(file_path, 'r', encoding='utf-8') as file:
      return [int(line.strip()) for line in file if line.strip().isdigit()]

  except FileNotFoundError:
    print(f"Arquivo não encontrado em: {file_path}")
    return []


# ---- COMUNICAÇÃO COM O CLIENTE ---- #
import json

def handle_client(conn, addr):
  """
  Função que realiza a interação e lida com os cliente que irão se conectar ao servidor.
  Envia todas as tarefas para os números perfeitos e depois para os amigáveis se ainda houver alguma.
  São enviados dados no formato json códificados em binário

  Keyword arguments:
    conn -- um socket que será ultilizado na comunicação entre o servidor e o cliente
    addr -- o endereço (HOST, PORT) do cliente que realizou a conexão, com quem a comunicação será realizada
  """

  try:
    task_send = None

    # Entra no contexto de controle do acesso protegido às fatias
    with CHUNK_LOCK:
      if task_chunks['perfects']:
        task_send = {
          "task_type": 'perfects',
          'payload': task_chunks['perfects'].pop(0)
        }

      elif task_chunks['friendly']:
        task_send = {
          "task_type": 'friendly',
          'payload': task_chunks['friendly'].pop(0)
        }

    if task_send is None:
      print("Não há mais fatias a serem resolvidas.")
      if conn:
        conn.close()
        print(f"Finalizando a conexão com o cliente: {addr}.")
      return
    
    print(f"Enviando para o cliente {addr} a fatia: {task_send}")

    # Converte a lista para o formato json e faz o encode dos dados em binário para serem enviados
    bytes_data = json.dumps(task_send).encode('utf-8')
    conn.sendall(bytes_data)

    # Espera os dados resolvidos, serem enviados ao servidor, assim realizando a decodificação e conversão para lista
    bytes_data = conn.recv(4096)
    if not bytes_data:
      raise ConnectionError(f"O cliente {addr} se desconectou antes de resolver a fatia {task_send}!")
    
    recv_data = json.loads(bytes_data.decode('utf-8'))

    with CHUNK_LOCK:
      # Junta os elementos já existentes ao recebidos
      final_data[recv_data["task_type"]].extend(recv_data["payload"])

  except ConnectionError as ce:
    print(ce)
  except Exception as e:
    print(f"Erro ao se comunicar com o cliente {addr}: {e}")

  finally:
    if conn:
      conn.close()
      print(f"Finalizando a conexão com o cliente: {addr}.")


# ---- CONFIGURAÇÃO E INICIALIZAÇÃO DO SERVIDOR ---- # 
from threading import Thread
import socket

HOST = '127.0.0.1'
PORT = 50000

def start_server(threads_list):
  """
  Configura o socket para poder realizar comunicações via protocolo TCP em redes de endereços IPv4 
  e realiza a associação do endereço local ao socket criado.
  Enquanto escuta no canal, fica disponivel para conexões, passando para as threads os sockets de comunicações, 
  permitindo realizar várias conexões
  
  Keyword arguments:
    thread_list -- uma lista para armazenar as threads para poder realizar a sincronização posteriormente
  """

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((HOST, PORT))

  server_socket.listen() 
  print(f"O Servidor está escutando no endereço {HOST}:{PORT}")

  try:

    for _ in range(num_chunks):
      conn, addr = server_socket.accept() 

      print(f"Conexão aceita com o cliente: {addr}")

      thread = Thread(target=handle_client, args=(conn, addr))
      thread.start()

      threads_list.append(thread)
    
  except Exception as e:
    print(f"Ocorreu um erro emquanto aceitava conexões! Erro: {e}")
  

# ---- DEFINIÇÃO DAS FATIAS (CHUNKS) ---- #
def gen_chunks(data, chunk_size):
  # 
  """
  Divide a lista de dados em fatias com base no tamanho da lista no total e no tamanho que cada fatia deve ter.

  Keyword arguments: 
    data -- uma lista que cotém os dados a serem dividos em fatias
    chunk_size -- o tamanho que cadafatia deverá ter

  Returns:
    chunks[list]: uma lista contendo todas as fatias, sendo essas parte da lista original
  """
  return [data[i:(i + chunk_size)] for i in range(0, len(data), chunk_size)]


# ---- DEFINIÇÃO DOS DADOS QUE SERÃO USADOS NO PROGRAMA ---- #
from math import ceil, floor
from sys import argv
from itertools import combinations

data_file = argv[2] if len(argv) > 2 else 'minimal_test.txt'    # Arquivo com os dados
data = read_data()                                              # Lista de valores de teste
num_chunks = int(argv[1]) if len(argv) > 1 else 8               # Quantidade de fatias (ou seja a quantidade de threads) [argumento 1 ou um valor default]

data_pair = list(combinations(data, 2))

chunks = gen_chunks(data, ceil(len(data) / floor(num_chunks/2)))
chunks_pair = gen_chunks(data_pair, ceil(len(data_pair) / floor(num_chunks/2)))

task_chunks = {'perfects': chunks, 'friendly': chunks_pair}


# ---- BLOCO DE EXECUÇÃO PRINCIPAL DO PROGRAMA ---- # 
from threading import Lock
CHUNK_LOCK = Lock() # Lock para proteger o acesso aos dados

final_data = {'perfects': [], 'friendly': []}
threads = []

start_server(threads)

print("Aguardando a finalização de todas as threads...")

# Esperando a finalização de cada thread
for thread in threads:
  thread.join()

print("\n# ---- RESULTADO FINAL DO PROBLEMA ---- #\n")
print(f"PERFEITOS: {final_data['perfects']}")
print(f"AMIGÁVEIS: {final_data['friendly']}")

final_data['perfects'] = [index[0] for index in final_data['perfects'] if index[1]]
final_data['friendly'] = [index[0] for index in final_data['friendly'] if index[1]]

with open('results.txt', 'w', encoding='utf-8') as results:
  results.write(f"NÚMEROS PERFEITOS: {final_data['perfects']}\nNÚMEROS AMIGÁVEIS: {final_data['friendly']}")