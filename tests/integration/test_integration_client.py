from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestWebhookIntegration: 
  
  def test_create_client_endpoint(self):
    payload = {
      "cliente_nome": "João",
      "cliente_email": "joao@email.com",
      "tipo_solicitacao": "Atualização cadastral",
      "valor_patrimonio": 250000
    }

    response = client.post(
      "/clientes", json=payload
    )

    assert response.status_code == 200

    body = response.json()

    assert body["cliente_email"] == "joao@email.com"