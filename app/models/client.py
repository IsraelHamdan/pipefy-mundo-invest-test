import uuid
from sqlalchemy.dialects.postgresql import UUID
from decimal import Decimal

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SqlEnum
from app.db.connection import Base
from app.enuns.client_enuns import (
    ClientPriority,
    ClientStatus
)

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(255))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    request_type: Mapped[str] = mapped_column(String(255))

    asset_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    status: Mapped[ClientStatus] = mapped_column(
        SqlEnum(ClientStatus)
    )

    priority: Mapped[ClientPriority | None] = mapped_column(
        SqlEnum(ClientPriority),
        nullable=True
    )

    pipefy_card_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )   