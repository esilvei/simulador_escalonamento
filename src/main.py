from models import Processo
from simulator import SimuladorEscalonamento
from utils import exibir_tabela_e_metricas, gerar_gantt

def main():
    SOBRECARGA_CONTEXTO = 1
    QUANTUM = 2

    processos_teste = [
        Processo(0, 0, 4, 1, 10),
        Processo(1, 2, 6, 2, 14),
        Processo(2, 4, 6, 3, 20),
        Processo(3, 6, 8, 4, 24)
    ]

    simulador = SimuladorEscalonamento(processos_teste, SOBRECARGA_CONTEXTO, QUANTUM)

    algoritmo_escolhido = "RR_PRIORIDADE_DINAMICA"

    print(f"Iniciando simulação: {algoritmo_escolhido}")

    concluidos, timeline, metricas_globais = simulador.executar(algoritmo_escolhido)
    tempo_total = timeline[-1][0] + 1 if timeline else 0

    exibir_tabela_e_metricas(concluidos, tempo_total, algoritmo_escolhido, metricas_globais)
    gerar_gantt(timeline, processos_teste, algoritmo_escolhido)

if __name__ == "__main__":
    main()