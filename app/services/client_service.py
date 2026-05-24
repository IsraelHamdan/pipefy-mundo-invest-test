from app.models.client import Client
from app.schema.client_schema import CreateClientDTO

from app.repositories.client_repository import ClientRepository

class ClientService: 
  def __init__(self):
    self.repository = ClientRepository()

  def create_client(self, db, data: CreateClientDTO):
      
      client = Client(
        name = data.name, 
        email = data.email, 
        request_type = data.request_type, 
        asset_value = data.asset_value, 
        status = "Aguardando Análise"
      )
      return self.repository.create(db, client)