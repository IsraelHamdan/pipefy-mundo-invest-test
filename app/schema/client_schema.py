import uuid

from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


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
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )

    cliente_email: EmailStr

    request_type: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )

    asset_value: Decimal | None = Field(
        default=None,
        gt=0
    )

    status: str | None = None

    priority: str | None = None


class ClientResponseDTO(BaseModel):
    id: uuid.UUID

    name: str

    cliente_email: EmailStr

    request_type: str

    asset_value: Decimal

    status: str

    priority: str | None

    model_config = ConfigDict(
        from_attributes=True
    )