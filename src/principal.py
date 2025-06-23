import time
import os
import sys 
import subprocess
from pathlib import Path

def execute_script(file_path):
    """Executa um script Python de um arquivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
        exec(code, globals())
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
    except Exception as e:
        print(f"Erro ao executar {file_path}: {e}")

def execute_distributed_scripts(base_dir, num_clients, data_file):
    """Executa o código distribuído com um servidor e múltiplos clientes."""
    script_dir = os.path.join(base_dir, "distributed_sockets")
    server_script = os.path.join(script_dir, "server.py")
    client_script = os.path.join(script_dir, "client.py")
    logs_dir = os.path.join(script_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Inicia o servidor
    print("Iniciando o servidor...")
    server_logfile = open(os.path.join(logs_dir, "server_logfile.txt"), 'w', encoding='utf-8')
    server_process = subprocess.Popen(
        [sys.executable, server_script, str(num_clients), data_file],
        stdout=server_logfile,
        stderr=subprocess.STDOUT
    )
    
    print("Aguardando o servidor inicializar...")
    time.sleep(2)  # Aguarda o servidor

    # Inicia os clientes
    client_processes = []
    client_logfiles = []
    print(f"Iniciando {num_clients} clientes...")
    for i in range(num_clients):
        client_logfile = open(os.path.join(logs_dir, f"client_logfile_{i+1}.txt"), 'w', encoding='utf-8')
        client_logfiles.append(client_logfile)
        client_process = subprocess.Popen(
            [sys.executable, client_script],
            stdout=client_logfile,
            stderr=subprocess.STDOUT
        )
        client_processes.append(client_process)

    # Aguarda os clientes finalizarem
    for proc in client_processes:
        proc.wait()

    # Aguarda o servidor finalizar
    server_process.wait()

    # Fecha os arquivos de log
    for logfile in client_logfiles:
        logfile.close()
    server_logfile.close()

def main():
    # Caminhos absolutos para os scripts
    base_dir = Path(__file__).resolve().parent
    script_parallel = os.path.join(base_dir, "parallel_threads", "parallel_solver.py")
    script_sequential = os.path.join(base_dir, "sequencial", "sequential_solver.py")
    data_file = "minimal_test.txt"  # Nome do arquivo de dados

    # Executa o script paralelo
    print("Executando o script paralelo...")
    start_time = time.perf_counter()
    execute_script(script_parallel)
    parallel_time = time.perf_counter() - start_time
    print(f"Tempo de execução do script paralelo: {parallel_time:.2f} segundos\n")

    # Executa o script sequencial
    print("Executando o script sequencial...")
    start_time = time.perf_counter()
    execute_script(script_sequential)
    sequential_time = time.perf_counter() - start_time
    print(f"Tempo de execução do script sequencial: {sequential_time:.2f} segundos\n")

    # Executa o código distribuído
    print("Executando o código distribuído...")
    start_time = time.perf_counter()
    execute_distributed_scripts(base_dir, num_clients=12, data_file=data_file)
    distributed_time = time.perf_counter() - start_time
    print(f"Tempo de execução do código distribuído: {distributed_time:.2f} segundos\n")

if __name__ == "__main__":
    main()
