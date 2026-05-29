from app.db.connection import SessionLocal
from app.models.client import Client
from app.models.webhook_event import WebhookEvent

import pytest


@pytest.fixture(autouse=True)
def clean_database():

    db = SessionLocal()

    db.query(WebhookEvent).delete()
    db.query(Client).delete()

    db.commit()

    yield

    db.query(WebhookEvent).delete()
    db.query(Client).delete()

    db.commit()
    db.close()