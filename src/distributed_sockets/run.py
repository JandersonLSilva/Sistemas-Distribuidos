import subprocess
import sys
import time

NUM_CLIENTS = 12                      # Quantidade de clientes
SERVER_SCRIPT_NAME = 'server.py'      # Nome do arquivo python do servidor
CLIENT_SCRIPT_NAME = 'client.py'      # Nome do arquivo python do cliente

"""
Script que abre váriios processos, um para o servidor e os outros para o cliente.
Esses processos executam os scripts que fazem a distribuição do problema em questão, com base no modelo cliente/servidor.
O 'Popen' abre um processo em si, que pode ser passado 3 argumentos, o 1º sendo um array contendo 
  o executável, o nome do arquivo a ser executado e o argumento para a execução,  o 2º informa o local para a saída padrão
  e o 3º o informa o local de saída para os erros, se for informado 'subprocess.STDOUT' a saída irá para a saída padrão
Ao terminar as execuções para cada cliente do total que é definido, espera-se o processo de servidor terminar, se ainda não for o caso
"""

python_exe = sys.executable

client_processes = []

print("# ---- INICIANDO O SERVIDOR ---- #")

server_logfile = open('logs/server_logfile.txt', 'w', encoding='utf-8')

try:
  server_process = subprocess.Popen(
    [python_exe, '-u', SERVER_SCRIPT_NAME, str(NUM_CLIENTS), "minimal_test.txt"],
    stdout=server_logfile,
    stderr=subprocess.STDOUT
  )
except Exception as e:
  print(f"Erro ao tentar abrir um processo para o script {SERVER_SCRIPT_NAME}: {e}")
  sys.exit(1)
  

print("\nAguardando 2 segundos para o servidor inicializar...")
time.sleep(2)

print(f"\n# ---- INICIANDO {NUM_CLIENTS} CLIENTES ---- #")
client_logfiles = []

while len(client_processes) < NUM_CLIENTS:
  client_logfile = open(f'logs/client_logfile_{len(client_processes)+1}.txt', 'w', encoding='utf-8')
  client_logfiles.append(client_logfile)
  try: 
    # Inicia cada cliente e seu próprio processo
    client_process = subprocess.Popen(
      [python_exe, '-u', CLIENT_SCRIPT_NAME],
      stdout=client_logfile,
      stderr=subprocess.STDOUT
    )
    client_processes.append(client_process)
    print(f"Processo atual: {len(client_processes)}")
  except Exception as e:
    print(f"Erro ao tentar abrir um processo para o script: {CLIENT_SCRIPT_NAME}")

# ---- FINALIZAÇÃO DOS PROCESSOS  ---- #

print("\n# ---- AGUARDANDO A FINALIZAÇÃO DOS CLIENTES ---- #")
for i, proc in enumerate(client_processes):
  proc.wait()

print("\n# ---- TODOS OS CLIENTES FINALIZARAM. ESPERANDO O SERVIDOR ENCERRAR... ---- #")
# server_process.terminate()
server_process.wait()

for client_logfile in client_logfiles:
  client_logfile.close()
server_logfile.close()

print("\n# ---- ENCERRADO. ---- #")