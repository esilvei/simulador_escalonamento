import copy


class SimuladorEscalonamento:
    def __init__(self, processos, sobrecarga_contexto, quantum=None):
        self.processos_originais = processos
        self.sobrecarga_contexto = sobrecarga_contexto
        self.quantum = quantum

    def executar(self, algoritmo):
        import copy
        processos = copy.deepcopy(self.processos_originais)
        processos.sort(key=lambda p: p.chegada)

        tempo_atual = 0
        fila_prontos = []
        processos_concluidos = []

        cpu_processo = None
        quantum_restante = 0
        sobrecarga_restante = 0
        ultimo_processo_id = None
        timeline = []

        ticks_ociosos = 0
        total_preempcoes = 0
        total_trocas_contexto = 0

        while processos or fila_prontos or cpu_processo or sobrecarga_restante > 0:
            if algoritmo == "RR_PRIORIDADE_DINAMICA":
                for p in fila_prontos:
                    p.tempo_na_fila += 1
                    # A cada 5 u.t. na fila, a prioridade melhora (diminui o valor)
                    if p.tempo_na_fila >= 5:
                        p.prioridade_dinamica = max(1, p.prioridade_dinamica - 1)
                        p.tempo_na_fila = 0

            # 1. Chegada de novos processos
            chegaram_agora = [p for p in processos if p.chegada == tempo_atual]
            for p in chegaram_agora:
                fila_prontos.append(p)
                processos.remove(p)

            # 2. Verifica conclusão
            if cpu_processo and cpu_processo.tempo_restante == 0:
                cpu_processo.tempo_termino = tempo_atual
                cpu_processo.calcular_metricas()
                processos_concluidos.append(cpu_processo)
                cpu_processo = None

            # 3. Lógica de Preempção
            if cpu_processo and sobrecarga_restante == 0:
                preemptar = False

                if algoritmo == "RR" and quantum_restante == 0:
                    preemptar = True
                elif algoritmo == "EDF":
                    if fila_prontos:
                        melhor_fila = min(fila_prontos, key=lambda p: p.deadline)
                        if melhor_fila.deadline < cpu_processo.deadline:
                            preemptar = True
                elif algoritmo == "RR_PRIORIDADE_DINAMICA":
                    # Preempta se o quantum acabar ou se chegar alguém com prioridade dinâmica superior
                    if quantum_restante == 0:
                        preemptar = True
                    elif fila_prontos:
                        melhor_fila = min(fila_prontos, key=lambda p: p.prioridade_dinamica)
                        if melhor_fila.prioridade_dinamica < cpu_processo.prioridade_dinamica:
                            preemptar = True

                if preemptar:
                    total_preempcoes += 1
                    fila_prontos.append(cpu_processo)
                    cpu_processo = None

            # 4. Seleção
            if not cpu_processo and sobrecarga_restante == 0 and fila_prontos:
                if algoritmo == "FIFO":
                    fila_prontos.sort(key=lambda p: p.chegada)
                elif algoritmo == "SJF":
                    fila_prontos.sort(key=lambda p: p.execucao)
                elif algoritmo == "PRIORIDADE":
                    fila_prontos.sort(key=lambda p: p.prioridade)
                elif algoritmo == "RR":
                    pass
                elif algoritmo == "EDF":
                    fila_prontos.sort(key=lambda p: p.deadline)
                elif algoritmo == "RR_PRIORIDADE_DINAMICA":
                    # Ordena primeiro pela melhor prioridade dinâmica, e depois por quem chegou antes
                    fila_prontos.sort(key=lambda p: (p.prioridade_dinamica, p.chegada))

                proximo = fila_prontos.pop(0)

                # Reset do envelhecimento ao ganhar a CPU
                if algoritmo == "RR_PRIORIDADE_DINAMICA":
                    proximo.prioridade_dinamica = proximo.prioridade
                    proximo.tempo_na_fila = 0

                # Contabiliza Troca de Contexto
                if ultimo_processo_id is not None and proximo.id != ultimo_processo_id:
                    sobrecarga_restante = self.sobrecarga_contexto
                    total_trocas_contexto += 1

                cpu_processo = proximo
                ultimo_processo_id = proximo.id
                quantum_restante = self.quantum

                if cpu_processo.tempo_inicio == -1:
                    cpu_processo.tempo_inicio = tempo_atual

            # 5. Execução do Tick Atual
            if sobrecarga_restante > 0:
                timeline.append((tempo_atual, "SOBRECARGA", ultimo_processo_id))
                sobrecarga_restante -= 1
            elif cpu_processo:
                if tempo_atual >= cpu_processo.deadline:
                    timeline.append((tempo_atual, "ESTOURO", cpu_processo.id))
                else:
                    timeline.append((tempo_atual, "EXEC", cpu_processo.id))
                cpu_processo.tempo_restante -= 1
                quantum_restante -= 1
            else:
                timeline.append((tempo_atual, "LIVRE", None))
                ticks_ociosos += 1

            tempo_atual += 1

        metricas_globais = {
            "ticks_ociosos": ticks_ociosos,
            "total_preempcoes": total_preempcoes,
            "total_trocas_contexto": total_trocas_contexto
        }

        return processos_concluidos, timeline, metricas_globais