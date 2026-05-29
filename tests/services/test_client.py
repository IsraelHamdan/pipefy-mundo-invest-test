from fastapi import HTTPException
from pydantic import ValidationError
import pytest
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService
from app.schema.client_schema import CreateClientDTO
from app.models.client import Client
from app.enuns.client_enuns import (
    Prioridade,
    Status
)
from unittest.mock import Mock
from unittest.mock import create_autospec
from decimal import Decimal
from app.services.pipefy_service import PipefyService

@pytest.fixture
def repository(): 
  return create_autospec(
    ClientRepository
  )

@pytest.fixture 
def pipefy_service(): 
  return create_autospec( 
    PipefyService
  )

class TestCreateClient:
  # teste de criação com sucesso
  def test_should_create_client_successfully(self, repository, pipefy_service):

    service = ClientService()
    service.repository = repository
    service.pipefy_service = pipefy_service

    repository.find_by_cliente_email.return_value = None 

    repository.create.return_value = Mock(
      cliente_nome = "Pedro",
      cliente_email="pedro@gmail.com",
      status=Status.AGUARDANDO_ANALISE
    )

    dto = CreateClientDTO(
      cliente_nome="Pedro", 
      cliente_email="pedro@gmail.com",
      tipo_solicitacao="Atualização de cadastro",
      valor_patrimonio=Decimal("45000")
    )

    result = service.create_client(db=None, data=dto)

    assert result.cliente_email == "pedro@gmail.com"

    assert(
      result.status == Status.AGUARDANDO_ANALISE
    )

    repository.create.assert_called_once()

    pipefy_service.build_create_card_mutation.assert_called_once_with(dto)

    repository.find_by_cliente_email.assert_called_once_with(
        None,
        "pedro@gmail.com"
    )

  # Teste de criação com e-mail duplicado
  def test_should_not_create_client_with_duplicate_email(
    self,
    repository,
    pipefy_service
  ): 
    service = ClientService()
    service.repository = repository
    service.pipefy_service = pipefy_service

    
    repository.find_by_cliente_email.return_value = Mock()

    dto = CreateClientDTO(
        cliente_nome="Pedro",
        cliente_email="pedro@gmail.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=Decimal("45000")
    )

    with pytest.raises(HTTPException) as exc: 
      service.create_client(db=None, data=dto)

    assert exc.value.status_code == 409

    assert(
      exc.value.detail == "Cliente já cadastrado com este e-mail"
    )

    repository.create.assert_not_called()

    pipefy_service.build_create_card_mutation.assert_not_called()


  # Caso de teste: Tenta criar com dados faltando
  def test_should_fail_when_email_is_missing(self):

    with pytest.raises(ValidationError):
      CreateClientDTO(
        cliente_nome="Pedro",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=Decimal("45000")
      ) # type: ignore

  # Caso de teste: email inválido
  def test_should_fail_when_email_is_invalid(self):

    with pytest.raises(ValidationError):
        CreateClientDTO(
            cliente_nome="Pedro",
            cliente_email="email-invalido",
            tipo_solicitacao="Atualização cadastral",
            valor_patrimonio=Decimal("45000")
        )