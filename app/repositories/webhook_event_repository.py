from sqlalchemy.orm import Session
from app.models.client import Client
from app.models.webhook_event import WebhookEvent


class WebhookEventRepository:

    def exists_by_event_id(
        self,
        db: Session,
        event_id: str
    ) -> bool:

        event = (
            db.query(WebhookEvent)
            .filter(WebhookEvent.event_id == event_id)
            .first()
        )

        return event is not None

    def create(
        self,
        db: Session,
        event_id: str
    ) -> WebhookEvent:

        event = WebhookEvent(
            event_id=event_id
        )

        db.add(event)

        db.commit()

        db.refresh(event)

        return event
    
    def find_by_email(
        self, 
        db: Session,
        email: str
    ) -> Client | None: 
        return(
            db.query(Client).filter(Client.email == email).first()
        )
    
    def update(
        self,
        db: Session,
        client: Client
    ) -> Client:

        db.commit()

        db.refresh(client)

        return client