import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def exibir_tabela_e_metricas(processos, timeline_length, nome_algoritmo, metricas_globais):
    dados = []
    for p in processos:
        dados.append({
            "ID": p.id,
            "Chegada": p.chegada,
            "Execução": p.execucao,
            "Deadline": p.deadline,
            "Prioridade": p.prioridade,
            "Início(s)": str(p.todos_inicios) if len(p.todos_inicios) > 1 else str(p.tempo_inicio),
            "Término": p.tempo_termino,
            "Espera": p.espera,
            "Turnaround": p.turnaround,
            "Deadline OK?": "Não" if p.estourou_deadline else "Sim"
        })

    df = pd.DataFrame(dados).sort_values("ID")
    print(f"\n--- Tabela Final: {nome_algoritmo} ---")
    print(df.to_string(index=False))

    # Cálculos das novas métricas exigidas
    media_espera = df["Espera"].mean()
    media_turnaround = df["Turnaround"].mean()
    throughput = len(processos) / timeline_length if timeline_length > 0 else 0
    perc_ociosidade = (metricas_globais['ticks_ociosos'] / timeline_length) * 100 if timeline_length > 0 else 0

    print("\n--- Resumo Quantitativo ---")
    print(f"Tempo total de simulação: {timeline_length} u.t.")
    print(f"Média de Espera: {media_espera:.2f}")
    print(f"Média de Turnaround: {media_turnaround:.2f}")
    print(f"Throughput: {throughput:.4f} processos/u.t.")
    print(f"% de CPU Ociosa: {perc_ociosidade:.2f}%")
    print(f"Total de Preempções: {metricas_globais['total_preempcoes']}")
    print(f"Total de Trocas de Contexto: {metricas_globais['total_trocas_contexto']}")
    return {
        "media_espera": media_espera,
        "media_turnaround": media_turnaround,
        "throughput": throughput,
        "pct_ociosa": perc_ociosidade,
    }

def gerar_gantt(timeline, processos_originais, nome_algoritmo):
    """Gera o Gráfico de Gantt exigido[cite: 42]."""
    fig, ax = plt.subplots(figsize=(12, 5))

    cores = {"EXEC": "green", "SOBRECARGA": "red", "ESTOURO": "gray"}

    pids = [p.id for p in processos_originais]
    ax.set_yticks(pids)
    ax.set_yticklabels([f"P{pid}" for pid in pids])
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Processos")
    ax.set_title(f"Gráfico de Gantt - {nome_algoritmo}")
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    if not timeline:
        return

    bloco_inicio = timeline[0][0]
    estado_atual = timeline[0][1]
    pid_atual = timeline[0][2]

    for i in range(1, len(timeline) + 1):
        tick = timeline[i] if i < len(timeline) else (timeline[-1][0] + 1, None, None)

        if tick[1] != estado_atual or tick[2] != pid_atual:
            duracao = tick[0] - bloco_inicio

            if estado_atual in cores and pid_atual is not None:
                ax.broken_barh([(bloco_inicio, duracao)],
                               (pid_atual - 0.4, 0.8),
                               facecolors=cores[estado_atual],
                               edgecolor='black')

            bloco_inicio = tick[0]
            estado_atual = tick[1]
            pid_atual = tick[2]

    for p in processos_originais:
        ax.vlines(x=p.deadline, ymin=p.id - 0.5, ymax=p.id + 0.5, colors='red', linestyles='solid', linewidth=2)

    legendas = [
        mpatches.Patch(color='green', label='Execução'),
        mpatches.Patch(color='red', label='Sobrecarga'),
        mpatches.Patch(color='gray', label='Estouro Deadline'),
        mpatches.mlines.Line2D([], [], color='red', marker='|', linestyle='None', markersize=10, markeredgewidth=2,
                               label='Deadline Absoluto')
    ]
    ax.legend(handles=legendas, loc="upper right")

    plt.tight_layout()
    # Salva a imagem com o nome do algoritmo
    plt.savefig(f"gantt_{nome_algoritmo}.png", dpi=300, bbox_inches='tight')
    plt.close(fig)