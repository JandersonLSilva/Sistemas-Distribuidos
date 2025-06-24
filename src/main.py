import time
import os
import sys
import subprocess
from pathlib import Path
import sys
from pathlib import Path

# Adiciona o diretório do plot_generator ao sys.path
BASE_DIR = Path(__file__).resolve().parent.parent  # Ajuste o caminho para o diretório base
ANALYSIS_DIR = BASE_DIR / "analysis"
sys.path.append(str(ANALYSIS_DIR))

from plot_generator import comparar_e_gerar_relatorio  # Importa a função do gerador de relatórios


def execute_script_subprocess(file_path):
    """Executa um script Python como um subprocesso e mede o tempo de execução."""
    start_time = time.perf_counter()
    try:
        subprocess.run([sys.executable, file_path], check=True)
    except FileNotFoundError:
        print(f"Arquivo {file_path} não encontrado.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {file_path}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao executar {file_path}: {e}")
    return time.perf_counter() - start_time

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

    # Coleta os tempos de execução
    resultados = {}

    print("Executando o script paralelo...")
    resultados["Threads Paralelas"] = {
        "tempo": execute_script_subprocess(script_parallel)
    }

    print("Executando o script sequencial...")
    resultados["Sequencial"] = {
        "tempo": execute_script_subprocess(script_sequential)
    }

    print("Executando o código distribuído...")
    start_time = time.perf_counter()
    execute_distributed_scripts(base_dir, num_clients=12, data_file=data_file)
    resultados["Sockets Distribuidos"] = {
        "tempo": time.perf_counter() - start_time
    }

    # Gera o relatório com os resultados
    comparar_e_gerar_relatorio(resultados)

if __name__ == "__main__":
    main()
