from decimal import Decimal
from sqlalchemy.orm import Session
from app.enuns.client_enuns import ClientPriority, ClientStatus
from app.repositories.client_repository import(
  ClientRepository
)
from app.repositories.webhook_event_repository import(
  WebhookEventRepository
)
from app.schema.webhook import PipefyWebhookDTO
from app.services.pipefy_service import PipefyService

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

    if already_processed: return {
      "message": "Event already processed"
    }

    client = (
      self.client.find_by_email(db, data.cliente_email)
    )

    if not client: 
      return {
        "message": "Client not found"
      }
    
    if client.asset_value >= Decimal("200000"):
      client.priority = ClientPriority.HIGH
    else:
        client.priority = ClientPriority.NORMAL
    
    client.status = ClientStatus.WAITING_ANALYSIS


    self.client.update(db, client)

    self.webhook.create(db, data.event_id)

    graphql_payload= (
      self.pipefy_service.build_update_card_mutation(
          data.card_id,
          ClientPriority.HIGH
      )
    )

    print(graphql_payload)

    return {
      "message": "Webhook processed"
    }

