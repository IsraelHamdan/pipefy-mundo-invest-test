from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.dependencies import getDB
from app.schema.client_schema import(ClientResponseDTO, CreateClientDTO)
from app.services.client_service import ClientService

router = APIRouter(
  prefix="/clientes",
  tags=["Clientes"]
)
service = ClientService()


@router.post(
  "",
  response_model= ClientResponseDTO
)
def create_client(
  data: CreateClientDTO,
  db: Session = Depends(getDB)
):
  client = service.create_client(db, data)

  return client