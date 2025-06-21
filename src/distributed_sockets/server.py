LOG_STRING = ""

# ---- LEITURA DO ARQUIVO COM OS DADOS ---- #
from pathlib import Path

def read_data():
  """
  Lê um arquivo com dados de teste e extrai todas as linhas que contém somente números.
  O caminho é resolvido de forma relativa.

  Returns:
    list[int]: Uma lista de números inteiros contendo os valores do arquivo
               Retorna uma lista vazia caso o arquivo não seja encontrado
  """

  # Resolução do caminho para o arquivo contendo valores para os testes
  file_path = (Path(__file__).parent / '..' / '..' / 'data' / 'minimal_test.txt').resolve()

  try:
    # Entra no contexto do arquivo que será aberto para leitura, com codificação utf-8
    with open(file_path, 'r', encoding='utf-8') as file:
      # Usando a compressão de lista para filtrar as linhas não numéricas e converte o restante para inteiro
      return [int(line.strip()) for line in file if line.strip().isdigit()]

  except FileNotFoundError:
    print(f"Arquivo não encontrado em: {file_path}")
    return []
  


# ---- CONFIGURAÇÃO E INICIALIZAÇÃO DO SERVIDOR ---- # 
import threading
import socket

HOST = '127.0.0.1'
PORT = 50000

def start_server(threads_list):
  """
  Configura o socket para poder realizar comunicações via protocolo TCP em redes de endereços IPv4 
  e realiza a associação do endereço local ao socket criado.
  Enquanto escuta no canal, fica disponivel para conexões, passando para as threads os sockets de comunicações, 
  permitindo realizar várias conexões
  
  Args:
  thread_list -- uma lista para armazenar as threads para poder realizar a sincronização posteriormente

  Não retorna nada.
  """

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((HOST, PORT))

  server_socket.listen() 
  print(f"O Servidor está escutando no endereço {HOST}:{PORT}")

  try:

    for _ in range(NUM_CHUNKS):
      conn, addr = server_socket.accept() 

      print(f"Conexão aceita com o cliente: {addr}")

      thread = threading.Thread(target=handle_client, args=(conn, addr))
      thread.start()

      threads_list.append(thread)
    
  except Exception as e:
    print(f"Ocorreu um erro emquanto aceitava conexões! Erro: {e}")
  


# ---- DEFINIÇÃO DAS FATIAS (CHUNKS) E INTERAÇÃO COM COM O CLIENTE ---- #
import json

def handle_client(conn, addr):
  """
  Função que realiza a interação e lida com os cliente que irão se conectar ao servidor

  Não retorna nada.
  """

  try:
    # Entra no contexto de controle do acesso protegido às fatias
    with CHUNK_LOCK:
      if not CHUNKS:
        print("Não há mais fatias a serem resolvidas")
        return
      
      current_chunk = CHUNKS.pop(0)
      print(f"Enviando para o cliente {addr} a fatia: {current_chunk}")

    # Converte a lista para o formato json e faz o encode dos dados em binário para serem enviados
    bytes_data = json.dumps(current_chunk).encode('utf-8')
    conn.sendall(bytes_data)


    # Espera os dados reolvidos, serem enviados ao servidor, assim realizando a decodificação e conversão para lista
    bytes_data = conn.recv(4096)
    if not bytes_data:
      raise ConnectionError(f"O cliente {addr} se desconectou antes de resolver a fatia {current_chunk}!")
    
    with CHUNK_LOCK:
      # Junta os elementos já existentes ao recebidos
      FINAL_DATA.extend(json.loads(bytes_data.decode('utf-8')))

  except Exception as e:
    print(f"Erro ao se comunicar com o cliente {addr}: {e}")

  finally:
    conn.close()
    print(f"Finalizando a conexão com o cliente: {addr}")


# ---- BLOCO DE EXECUÇÃO PRINCIPAL DO PROGRAMA ---- # 
import math
import sys

num_chunks_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8

DATA = read_data()                                            # Lista de valores de teste
DATA_LENGHT = len(DATA)                                       # Tamanho da lista
NUM_CHUNKS = int(sys.argv[1]) if len(sys.argv) > 1 else 8     # Quantidade de fatias (ou seja a quantidade de threads) [argumento 1 ou um valor default]
CHUNK_SIZE = math.ceil(DATA_LENGHT / NUM_CHUNKS)              # Tamanho da fatia

print(DATA)

# Divide a lista de dados em fatias para serem resolvidas
CHUNKS = [DATA[i:(i + CHUNK_SIZE)] for i in range(0, len(DATA), CHUNK_SIZE)]
print(CHUNKS)

CHUNK_LOCK = threading.Lock() # Lock proteger o acesso aos dados
FINAL_DATA = []
threads = []

start_server(threads)

print("Aguardando a finalização de todas as threads...")

# Esperando a finalização de cada thread
for thread in threads:
  thread.join()

print(f"\n# ---- RESULTADO FINAL DO PROBLEMA ---- #\n{FINAL_DATA}")