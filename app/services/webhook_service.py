from decimal import Decimal
from sqlalchemy.orm import Session
from app.enuns.client_enuns import Prioridade, Status
from app.repositories.client_repository import(
  ClientRepository
)
from app.repositories.webhook_event_repository import(
  WebhookEventRepository
)
from app.schema.webhook import PipefyWebhookDTO
from app.services.pipefy_service import PipefyService
from fastapi import HTTPException
import logging

class WebhookService: 
  def __init__(self):
    self.pipefy_service = PipefyService()
    self.webhook = (
        WebhookEventRepository()
    )
    self.client = ClientRepository()

  
  def process_card_updated(self, db:Session, data: PipefyWebhookDTO):
    already_processed = (
      self.webhook.exists_by_event_id(db, data.event_id)
    )

    if already_processed:
      raise HTTPException(
          status_code=409,
          detail="Event already processed"
      )


    client = (
      self.client.find_by_cliente_email(db, data.cliente_email)
    )

    if not client:
      raise HTTPException(
          status_code=404,
          detail="Client not found"
      )
    
    prioridade: Prioridade

    if client.valor_patrimonio >= Decimal("200000"):
        prioridade = Prioridade.PRIORIDADE_ALTA
    else:
        prioridade = Prioridade.PRIORIDADE_NORMAL

    client.prioridade = prioridade
    client.status = Status.PROCESSADO

    self.client.update(db, client)

    self.webhook.create(db, data.event_id)

    graphql_payload = self.pipefy_service.build_update_fields_values_mutation(
        data.card_id,
        prioridade
    )

    logger = logging.getLogger(__name__)

    logger.info(
        "Pipefy mutation generated",
        extra={"payload": graphql_payload}
    )
    
    return {
      "message": "Webhook processed"
    }
