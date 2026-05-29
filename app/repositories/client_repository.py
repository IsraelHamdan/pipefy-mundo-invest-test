from sqlalchemy.orm import Session

from app.models.client import Client


class ClientRepository:

    def create(self, db: Session, client: Client) -> Client:
        db.add(client)

        db.commit()

        db.refresh(client)

        return client

    def find_by_cliente_email(
        self,
        db: Session,
        cliente_email: str
    ) -> Client | None:

        return (
            db.query(Client)
            .filter(Client.cliente_email == cliente_email)
            .first()
        )

    def update(
        self,
        db: Session,
        client: Client
    ) -> Client:

        db.commit()

        db.refresh(client)

        return client
