from sqlalchemy.orm import Session

from app.models.client import Client


class ClientRepository:

    def create(self, db: Session, client: Client) -> Client:
        db.add(client)

        db.commit()

        db.refresh(client)

        return client