from sqlalchemy.orm import Session

from app.models.client import Client


class ClientRepository:

    def create(self, db: Session, client: Client) -> Client:
        db.add(client)

        db.commit()

        db.refresh(client)

        return client

    def find_by_email(
        self,
        db: Session,
        email: str
    ) -> Client | None:

        return (
            db.query(Client)
            .filter(Client.email == email)
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