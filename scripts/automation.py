import sys
import os
import copy
from pathlib import Path

from src.models import Processo
from src.simulator import SimuladorEscalonamento
from src.utils import exibir_tabela_e_metricas, gerar_gantt


def main_automacao():
    # --- Configuração de Diretórios ---
    # Descobre a pasta atual do script (scripts/) e define a pasta alvo (data/)
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"

    # Garante que a pasta 'data' exista
    data_dir.mkdir(parents=True, exist_ok=True)

    # Muda o diretório de trabalho do script para a pasta 'data'.
    # Isso faz com que todos os arquivos (txt e png) sejam salvos lá.
    os.chdir(data_dir)
    # ----------------------------------

    # Parâmetros Globais da Simulação
    SOBRECARGA_CONTEXTO = 1
    QUANTUM = 2

    # id, chegada, execucao, prioridade, deadline
    processos_base = [
        Processo(0, 0, 4, 1, 10),
        Processo(1, 2, 6, 2, 14),
        Processo(2, 4, 6, 3, 20),
        Processo(3, 6, 8, 4, 24)
    ]

    lista_algoritmos = [
        "FIFO",
        "SJF",
        "PRIORIDADE",
        "RR",
        "EDF",
        "RR_PRIORIDADE_DINAMICA"
    ]

    arquivo_saida = "resultados_relatorio.txt"

    print(f"Iniciando automação... Os resultados serão salvos em: {data_dir.absolute()}")

    # Redireciona a saída padrão (sys.stdout) para um arquivo de texto
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        console_original = sys.stdout
        sys.stdout = f

        for algoritmo in lista_algoritmos:
            print(f"\n{'=' * 50}")
            print(f" SIMULAÇÃO: {algoritmo} ")
            print(f"{'=' * 50}")

            processos_teste = copy.deepcopy(processos_base)

            simulador = SimuladorEscalonamento(processos_teste, SOBRECARGA_CONTEXTO, QUANTUM)
            concluidos, timeline, metricas_globais = simulador.executar(algoritmo)

            tempo_total = timeline[-1][0] + 1 if timeline else 0

            exibir_tabela_e_metricas(concluidos, tempo_total, algoritmo, metricas_globais)

            gerar_gantt(timeline, processos_teste, algoritmo)

            sys.stdout = console_original
            print(f"-> {algoritmo} concluído! Gráfico salvo em 'data/'.")
            sys.stdout = f

        sys.stdout = console_original


if __name__ == "__main__":
    main_automacao()