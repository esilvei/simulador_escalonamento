import sys
import os
import copy
import time
import platform
from pathlib import Path

raiz_projeto = str(Path(__file__).parent.parent)
sys.path.append(raiz_projeto)

from src.models import Processo
from src.simulator import SimuladorEscalonamento
from src.utils import exibir_tabela_e_metricas, gerar_gantt


def main_automacao():
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"

    data_dir.mkdir(parents=True, exist_ok=True)

    os.chdir(data_dir)

    SOBRECARGA_CONTEXTO = 1
    QUANTUM = 2

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
    arquivo_benchmark = "benchmark_tempos.txt"

    print(f"Iniciando automação... Os arquivos serão salvos em: {data_dir.absolute()}")

    inicio_real = time.time()

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

    fim_real = time.time()
    tempo_processamento = (fim_real - inicio_real) * 1000  # em ms

    sistema = platform.system()
    info_extra = platform.release()

    with open(arquivo_benchmark, "a", encoding="utf-8") as fb:
        fb.write(f"Ambiente: {sistema} ({info_extra}) | Tempo Físico: {tempo_processamento:.2f} ms\n")

    print("\n✅ Automação finalizada com sucesso!")
    print(f"Tempo de execução ({sistema}): {tempo_processamento:.2f} ms")
    print(f"O comparativo de tempo foi salvo/atualizado em 'data/{arquivo_benchmark}'.")


if __name__ == "__main__":
    main_automacao()