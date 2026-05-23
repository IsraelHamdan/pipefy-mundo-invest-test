from decimal import Decimal

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.connection import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True
    )

    request_type: Mapped[str] = mapped_column(String(255))

    asset_value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    status: Mapped[str] = mapped_column(String(100))

    priority: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )