from app.models.client import Client
from app.schema.client_schema import CreateClientDTO
from app.services.pipefy_service import PipefyService

from app.repositories.client_repository import ClientRepository


class ClientService: 
  def __init__(self):
    self.repository = ClientRepository()
    self.pipefy_serice = PipefyService()

  def create_client(self, db, data: CreateClientDTO):
      
      client = Client(
        name = data.cliente_nome, 
        email = data.cliente_email, 
        request_type = data.tipo_solicitacao, 
        asset_value = data.valor_patrimonio, 
        status = "Aguardando Análise"
      )

      graphql_payload = (
         self.pipefy_serice.build_create_card_mutation(data)
      )

      print(graphql_payload)

      return self.repository.create(db, client)