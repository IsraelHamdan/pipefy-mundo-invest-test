import uuid

from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateClientDTO(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=255
    )

    email: EmailStr

    request_type: str = Field(
        min_length=3,
        max_length=255
    )

    asset_value: Decimal = Field(gt=0)


class UpdateClientDTO(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )

    email: EmailStr | None = None

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

    email: EmailStr

    request_type: str

    asset_value: Decimal

    status: str

    priority: str | None

    model_config = ConfigDict(
        from_attributes=True
    )