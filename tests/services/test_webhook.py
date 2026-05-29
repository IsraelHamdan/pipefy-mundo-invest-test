import pytest

from unittest.mock import Mock
from unittest.mock import create_autospec

from decimal import Decimal

from app.enuns.client_enuns import Prioridade, Status
from app.services.webhook_service import WebhookService
from app.repositories.client_repository import ClientRepository
from app.repositories.webhook_event_repository import WebhookEventRepository
from app.services.pipefy_service import PipefyService


@pytest.fixture
def client_repository():
  return create_autospec(ClientRepository)

@pytest.fixture
def webhook_repository():
    return create_autospec(WebhookEventRepository)

@pytest.fixture
def pipefy_service():
    return create_autospec(PipefyService)

class TestWebhookTests: 
    def test_should_set_high_priority_when_patrimony_is_above_200k(self, 
        webhook_repository, 
        client_repository,
        pipefy_service
    ):
        fake_db = Mock()
        service = WebhookService()
        service.client = client_repository
        service.pipefy_service = pipefy_service
        service.webhook = webhook_repository

        client = Mock(   
            cliente_email="pedro@gmail.com",
            valor_patrimonio=Decimal("250000")

        )

        client_repository.find_by_cliente_email.return_value = client
        webhook_repository.exists_by_event_id.return_value = False

        payload = Mock(
            event_id="evt_123",
            card_id="card_456",
            cliente_email="pedro@gmail.com"
        )

        service.process_card_updated(
            db=fake_db,
            data=payload
        )

        assert (
            client.prioridade
            == Prioridade.PRIORIDADE_ALTA
        )

        assert (
            client.status
            == Status.PROCESSADO
        )

        client_repository.update.assert_called_once()

        webhook_repository.create.assert_called_once()

        pipefy_service.build_update_fields_values_mutation.assert_called_once_with(
            "card_456",
            Prioridade.PRIORIDADE_ALTA
        )