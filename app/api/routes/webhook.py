from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import getDB
from app.schema.webhook import PipefyWebhookDTO
from app.services.webhook_service import WebhookService

router = APIRouter(
    prefix="/webhooks/pipefy",
    tags=["Pipefy Webhooks"]
)

service = WebhookService()


@router.post("/card-updated")
def card_updated(
    data: PipefyWebhookDTO,
    db: Session = Depends(getDB)
):
    return service.process_card_updated(
        db,
        data
    )