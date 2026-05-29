import uuid
from sqlalchemy.dialects.postgresql import UUID
from decimal import Decimal

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Enum as SqlEnum
from app.db.connection import Base
from app.enuns.client_enuns import (
    Prioridade,
    Status
)


def enum_values(enum_cls):
    return [item.value for item in enum_cls]


class Client(Base):
    __tablename__ = "clientes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    cliente_nome: Mapped[str] = mapped_column(String(255))

    cliente_email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    tipo_solicitacao: Mapped[str] = mapped_column(String(255))

    valor_patrimonio: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    status: Mapped[Status] = mapped_column(
        SqlEnum(
            Status,
            name="cliente_status",
            values_callable=enum_values,
            validate_strings=True
        )
    )

    prioridade: Mapped[Prioridade | None] = mapped_column(
        SqlEnum(
            Prioridade,
            name="cliente_prioridade",
            values_callable=enum_values,
            validate_strings=True
        ),
        nullable=True
    )

    pipefy_card_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )   
