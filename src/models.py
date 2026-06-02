class Processo:
    def __init__(self, id_proc, chegada, execucao, prioridade, deadline):
        self.id = id_proc
        self.chegada = chegada
        self.execucao = execucao
        self.prioridade = prioridade
        self.deadline = deadline

        self.tempo_restante = execucao
        self.tempo_inicio = -1
        self.tempo_termino = -1

        self.turnaround = 0
        self.espera = 0
        self.estourou_deadline = False

        self.prioridade_dinamica = prioridade
        self.tempo_na_fila = 0

    def calcular_metricas(self):
        """Calcula turnaround e espera após a conclusão."""
        if self.tempo_termino != -1:
            self.turnaround = self.tempo_termino - self.chegada
            self.espera = self.turnaround - self.execucao
            self.estourou_deadline = self.tempo_termino > self.deadline

    def __repr__(self):
        return f"P{self.id}"