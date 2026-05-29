from enum import Enum


class Prioridade(str, Enum):
    PRIORIDADE_ALTA = "prioridade_alta"
    PRIORIDADE_NORMAL = "prioridade_normal"


class Status(str, Enum):
    AGUARDANDO_ANALISE = "Aguardando Análise"
    PROCESSADO = "Processado"
