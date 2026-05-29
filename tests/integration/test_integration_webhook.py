from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
import uuid

class TestWebhookIntegration:

    def test_card_update_pipefy(self):
        email = f"{uuid.uuid4()}@test.com"
        event_id = f"evt_{uuid.uuid4()}"
        # Arrange
        client.post(
            "/clientes",
            json={
                "cliente_nome": "João",
                "cliente_email": email,
                "tipo_solicitacao": "Atualização cadastral",
                "valor_patrimonio": 250000
            }
        )

        # Act
        response = client.post(
            "/webhooks/pipefy/card-updated",
            json={
                "event_id": event_id,
                "card_id": "card_001",
                "cliente_email": email,
                "timestamp": "2026-05-29T12:00:00Z"
            }
        )

        # Assert
        assert response.status_code == 200

        assert response.json() == {
            "message": "Webhook processed"
        }

    def test_should_not_process_same_event_twice(self): 

        email = f"{uuid.uuid4()}@test.com"

        event_id = "evt_duplicate_test"

        client.post(
            "/clientes",
            json={
                "cliente_nome": "João",
                "cliente_email": email,
                "tipo_solicitacao": "Atualização cadastral",
                "valor_patrimonio": 250000
            }
        )

        first_response = client.post(
            "/webhooks/pipefy/card-updated",
            json={
                "event_id": event_id,
                "card_id": "card_001",
                "cliente_email": email,
                "timestamp": "2026-05-29T12:00:00Z"
            }
        )

        second_response = client.post(
            "/webhooks/pipefy/card-updated",
            json={
                "event_id": event_id,
                "card_id": "card_001",
                "cliente_email": email,
                "timestamp": "2026-05-29T12"
            }
        )