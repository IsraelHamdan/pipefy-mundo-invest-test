from app.models.client import Client
from app.enuns.client_enuns import Status
from app.schema.client_schema import CreateClientDTO
from app.services.pipefy_service import PipefyService
from fastapi import HTTPException
from app.repositories.client_repository import ClientRepository
import logging


class ClientService: 
  def __init__(self):
    self.repository = ClientRepository()
    self.pipefy_service = PipefyService()

  def create_client(self, db, data: CreateClientDTO):
    
      self.email_already_exists(db, data.cliente_email)

      client = Client(
        cliente_nome = data.cliente_nome,
        cliente_email = data.cliente_email,
        tipo_solicitacao = data.tipo_solicitacao,
        valor_patrimonio = data.valor_patrimonio,
        status = Status.AGUARDANDO_ANALISE
      )

      # NOTE: Em produção o print deve ser removido e a integração com o pipefy deve ser realizada
      graphql_payload = (
         self.pipefy_service.build_create_card_mutation(data)
      )

      logger = logging.getLogger(__name__)
      logger.info(
        "Card created",
        extra={
          "payload": graphql_payload
        }
      )

      return self.repository.create(db, client)
  
  
  
  def email_already_exists(self, db, email: str) -> bool: 
    client = (
      self.repository.find_by_cliente_email(db, email)
    )

    if client: 
      raise HTTPException(
        status_code=409,
        detail="Cliente já cadastrado com este e-mail"
      )
    return False

