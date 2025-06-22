# Importação de bibliotecas necessárias
import subprocess  # Para executar scripts externos em Python
import time        # Para medir tempo de execução
import matplotlib.pyplot as plt  # Para gerar gráficos
from pathlib import Path  # Para trabalhar com caminhos de arquivos
from reportlab.lib.pagesizes import A4  # Tamanho da página para o PDF
from reportlab.pdfgen import canvas  # Para criar o PDF
from reportlab.lib.utils import ImageReader  # Para inserir imagens no PDF

# Define o caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos para salvar os gráficos e o PDF
IMG_BARRAS = BASE_DIR / "analysis/images/execution_times_graph.png"
IMG_LINHA = BASE_DIR / "analysis/images/execution_times_graph_line.png"
PDF_RELATORIO = BASE_DIR / "analysis/relatorio_resultados.pdf"

# Nomes dos algoritmos e os caminhos dos seus scripts
scripts = {
    "Sockets Distribuidos": BASE_DIR / "src/distributed_sockets/run.py",
    "Threads Paralelas": BASE_DIR / "src/parallel_threads/parallel_solver.py",
    "Sequencial": BASE_DIR / "src/sequencial/sequential_solver.py"
}

# Função que executa o script e mede seu tempo de execução
def medir_execucao(script_path):
    inicio = time.time()  # Marca o início
    try:
        resultado = subprocess.run(  # Executa o script
            ["python", script_path],
            capture_output=True,  # Captura a saída do terminal
            text=True,            # Retorna como texto
            check=True            # Retorna uma exceção se o script falhar
        )
        fim = time.time()  # Marca o fim
        return {
            "tempo": fim - inicio,             # Tempo total
            "saida": resultado.stdout.strip()  # Saída do script
        }
    except subprocess.CalledProcessError as e:
        return {
            "tempo": None,
            "saida": f"Erro ao executar {script_path}:\n{e.stderr.strip()}"
        }

# Função para gerar os gráficos com os tempos de execução
def gerar_graficos(resultados):
    nomes = []  # Lista com nomes dos algoritmos
    tempos = []  # Lista com os tempos correspondentes

    # Extrai os dados
    for nome, dados in resultados.items():
        if dados["tempo"] is not None:
            nomes.append(nome)
            tempos.append(dados["tempo"])

    # Gráfico de barras
    plt.figure(figsize=(8, 4))
    plt.bar(nomes, tempos, color='royalblue')
    plt.title("Tempo de Execução por Algoritmo (Barras)")
    plt.xlabel("Algoritmo")
    plt.ylabel("Tempo (s)")
    plt.tight_layout()
    plt.savefig(IMG_BARRAS)  # Salva o gráfico de barras
    plt.close()

    # Gráfico de linha
    plt.figure(figsize=(8, 4))
    plt.plot(nomes, tempos, marker='o', linestyle='-', color='darkorange')
    plt.title("Tempo de Execução por Algoritmo (Linha)")
    plt.xlabel("Algoritmo")
    plt.ylabel("Tempo (s)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(IMG_LINHA)  # Salva o gráfico de linha
    plt.close()

# Função que gera o PDF com os tempos e os gráficos
def gerar_pdf(resultados):
    c = canvas.Canvas(str(PDF_RELATORIO), pagesize=A4)  # Cria o PDF
    largura, altura = A4
    y = altura - 50  # Posição vertical inicial

    # Título do PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Relatório de Execução de Algoritmos")
    y -= 40

    # Insere os tempos de execução
    c.setFont("Helvetica", 12)
    for nome, dados in resultados.items():
        tempo = dados["tempo"]
        c.drawString(50, y, f"{nome}:")
        y -= 20
        if tempo is not None:
            c.drawString(70, y, f"Tempo de execução: {tempo:.6f} segundos")
        else:
            c.drawString(70, y, "Erro ao executar o algoritmo.")
        y -= 30  # Espaço entre os algoritmos

    # Insere o gráfico de barras no PDF
    if IMG_BARRAS.exists():
        c.showPage()  # Nova página
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, altura - 50, "Gráfico de Barras: Tempo por Algoritmo")
        imagem = ImageReader(str(IMG_BARRAS))
        c.drawImage(imagem, 50, altura / 2 - 100, width=500, preserveAspectRatio=True)

    # Insere o gráfico de linha no PDF
    if IMG_LINHA.exists():
        c.showPage()  # Nova página
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, altura - 50, "Gráfico de Linha: Tempo por Algoritmo")
        imagem = ImageReader(str(IMG_LINHA))
        c.drawImage(imagem, 50, altura / 2 - 100, width=500, preserveAspectRatio=True)

    c.save()  # Salva o PDF

# Função principal que executa os scripts, coleta os dados e gera os relatórios
def comparar_e_gerar_relatorio():
    resultados = {}
    for nome, caminho in scripts.items():
        print(f"\nExecutando: {nome}")
        dados = medir_execucao(str(caminho))  # Executa o script e coleta os dados dos algoritmos
        resultados[nome] = dados
        if dados["tempo"] is not None:
            print(f"{nome}: {dados['tempo']:.6f} segundos")
        else:
            print(f"{nome}: falhou na execução")

    gerar_graficos(resultados)  # Gera os gráficos com os resultados
    gerar_pdf(resultados)       # Gera o PDF com os resultados e os gráficos

#Executa o algoritmo
if __name__ == "__main__":
    comparar_e_gerar_relatorio()