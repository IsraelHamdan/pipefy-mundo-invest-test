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
cp .env.example .env

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

```bash
docker compose up --build -d
```

A API ficará disponível em:

<http://localhost:8000/docs#/>

Se quiser acompanhar os logs da api basta

```bash
docker compose logs -f api
```

---

#### 2. Criar ambiente para testes localmente

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

Afim de faciltar também dockerizei os testes, criando um container separado,
basta executar o comando depois que o docker terminar de subir os containers da aplicação:

```bash
docker compose run --rm tests
```

**Para executar os testes localmente** é necessário criar um ambiente virtual Python e instalar as dependências do projeto e mudar a url de conexão do banco dentro do .env, pois como a api e o python estão rodando dentro do docker eles conversam pelo nome do serviço e não por localhost, então basta na url de conexão substituir @pgsql:5432 por @localhost:5432, mas **se for rodar localmente!**

```bash
pytest -vv
```

Cobertura implementada:

✓ 7 testes unitários
✓ 4 testes de integração
✓ 11 testes automatizados

---

# Documentação 🐍

Swagger:

```text
http://localhost:8000/docs#/
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

```bash
curl -X POST http://localhost:8000/clientes \
-H "Content-Type: application/json" \
-d '{
  "cliente_nome":"João Silva",
  "cliente_email":"joao.silva@example.com",
  "tipo_solicitacao":"Atualização cadastral",
  "valor_patrimonio":250000
}'
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

```bash
curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
-H "Content-Type: application/json" \
-d '{
  "event_id":"evt_123",
  "card_id":"card_456",
  "cliente_email":"joao.silva@example.com",
  "timestamp":"2026-05-29T12:00:00Z"
}'
```

### Regras de Negócio

#### Patrimônio >= R$ 200.000

```text
Prioridade: prioridade_alta
Status: Processado
```

#### Patrimônio < R$ 200.000

```text
Prioridade: prioridade_normal
Status: Processado
```

#### Idempotência

Eventos já processados são ignorados através do controle por `event_id`.

---

# AWS

- API Gateway para expor os endpoints
- ECS Fargate para executar os containers da aplicação
- RDS PostgreSQL para armazenar clientes e eventos processados
- CloudWatch para logs e monitoramento
- Secrets Manager para credenciais
- Auto Scaling para lidar com aumento de tráfego

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
