from datetime import datetime
from pydantic import BaseModel


class PipefyWebhookDTO(BaseModel):
  event_id: str
  card_id: str
  cliente_email: str
  timestamp: datetime