from enum import Enum


class ClientPriority(str, Enum):
    HIGH = "Alta"
    NORMAL = "Normal"


class ClientStatus(str, Enum):
    WAITING_ANALYSIS = "Aguardando Análise"
    IN_ANALYSIS = "Em Análise"
    APPROVED = "Aprovado"
    REJECTED = "Rejeitado"