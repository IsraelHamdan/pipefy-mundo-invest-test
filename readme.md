# Pipefy Mundo Invest - Desafio Técnico Backend

## Sobre o Projeto

Esta aplicação foi desenvolvida como solução para o desafio técnico Backend da Mundo Invest.

O sistema simula a integração entre uma API interna de clientes e o Pipefy através da geração de mutations GraphQL, permitindo:

- Cadastro de clientes;
- Processamento de eventos recebidos via webhook;
- Classificação automática de prioridade;
- Controle de idempotência de eventos;
- Persistência dos dados em PostgreSQL.

---

## Tecnologias Utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 17
- Docker
- Pytest
- Pydantic

---

## Arquitetura ⚡

O projeto foi organizado em camadas para separar responsabilidades:

```text
app/
├── api/
├── db/
├── models/
├── repositories/
├── schema/
├── services/
└── core/
```

### Responsabilidades

| Camada        | Responsabilidade                 |
| ------------- | -------------------------------- |
| API           | Endpoints HTTP                   |
| Schema        | Validação de entrada e saída     |
| Service       | Regras de negócio                |
| DB            | Conexão com o Banco de Dados     |
| Repository    | Persistência de dados            |
| Models        | Entidades do banco               |
| PipefyService | Construção das mutations GraphQL |

---

# Executando o Projeto 🚀

## Pré-requisitos

- Docker Desktop
- Python 3.12+

---

### 1. Clonar o repositório

```bash
git clone https://github.com/IsraelHamdan/pipefy-mundo-invest-test.git
cd pipefy-mundo-invest-test
```

---

### 2. Criar arquivo env

Linux 🐧 / Mac 🍎

```bash
cp .env.exemple .env

```

Windows 🪟

```bash
copy .env.example .env
```

ou

```bash
Copy-Item .env.example .env
```

---

### 3. Subir aplicação usando Docker

Subir toda a aplicação:

docker compose up --build -d

A API ficará disponível em:

<http://localhost:8000/docs#/>

Se quiser acompanhar os logs da api basta

```bash
docker compose logs -f api
```

---

#### 2. Criar anbiente para testes localmente

##### Windows -

```bash
python -m venv .venv
.venv\Scripts\activate
```

##### Linux/macOS

```bash
python3 -m venv .venv

source .venv/bin/activate

```

---

##### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Executando testes 🧪

Para executar os testes localmente é necessário criar um ambiente virtual Python e instalar as dependências do projeto.

```bash
pytest -vv
```

Cobertura implementada:

✓ 7 testes unitários
✓ 2 testes de integração
✓ 9 testes automatizados

---

# Documentação 🐍

Swagger:

```text
http://localhost:8000/docs
```

---

# Endpoint - Cadastro de Cliente

## POST /clientes

### Request

```json
{
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000
}
```

### Regras

- E-mail deve ser único;
- Cliente inicia com status "Aguardando Análise";
- Mutation GraphQL de criação de card é gerada.

---

# Endpoint - Webhook Pipefy

## POST /webhooks/pipefy/card-updated

### Request

```json
{
  "event_id": "evt_123",
  "card_id": "card_456",
  "cliente_email": "joao.silva@example.com",
  "timestamp": "2026-05-29T12:00:00Z"
}
```

### Regras de Negócio

### Patrimônio >= R$ 200.000

```text
Prioridade: prioridade_alta
Status: Processado
```

### Patrimônio < R$ 200.000

```text
Prioridade: prioridade_normal
Status: Processado
```

### Idempotência

Eventos já processados são ignorados através do controle por `event_id`.

---

# Integração Pipefy

A integração foi simulada através da construção das mutations GraphQL conforme solicitado pelo desafio.

## Mutation de Criação

```graphql
createCard
```

Utilizada no cadastro do cliente.

---

## Mutation de Atualização

```graphql
updateFieldsValues
```

Utilizada para atualização dos campos de status e prioridade após o processamento do webhook.

---

# Testes

Executar todos os testes:

```bash
pytest -vv
```

Resultado atual:

```text
9 passed
```

## Testes Unitários

### Cliente

- Criação com sucesso;
- E-mail duplicado;
- E-mail inválido;
- Campo obrigatório ausente.

### Webhook

- Prioridade alta;
- Prioridade normal;
- Evento duplicado (idempotência).

## Testes de Integração

- POST /clientes;
- POST /webhooks/pipefy/card-updated.

---

# Melhorias Futuras para produção

Em um ambiente produtivo seriam considerados:

- Alembic para versionamento de banco;
- Integração real com a API GraphQL do Pipefy;
- Logs estruturados;
- CI/CD;
- Deploy em AWS;
- Monitoramento e observabilidade.

---

# Autor

Israel Hamdan
