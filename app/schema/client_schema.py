import uuid

from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.enuns.client_enuns import Prioridade, Status


class CreateClientDTO(BaseModel):

    cliente_nome: str = Field(
        min_length=3,
        max_length=255
    )

    cliente_email: EmailStr 

  
    tipo_solicitacao: str = Field(
        min_length=3,
        max_length=255
    )


    valor_patrimonio: Decimal = Field(gt=0)


class UpdateClientDTO(BaseModel):
    cliente_nome: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )

    cliente_email: EmailStr
    cliente_email: EmailStr

    tipo_solicitacao: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )

    valor_patrimonio: Decimal | None = Field(
        default=None,
        gt=0
    )

    status: Status | None = None

    prioridade: Prioridade | None = None


class ClientResponseDTO(BaseModel):
    id: uuid.UUID

    cliente_nome: str

    cliente_email: EmailStr
    cliente_email: EmailStr

    tipo_solicitacao: str

    valor_patrimonio: Decimal

    status: Status

    prioridade: Prioridade | None

    model_config = ConfigDict(
        from_attributes=True
    )
