# Pipefy Mundo Invest - Desafio Técnico Backend

## Sobre o Projeto

Esta aplicação foi desenvolvida como solução para o desafio técnico Backend da Mundo Invest.

O sistema simula a integração entre uma API interna de clientes e o Pipefy através da geração de mutations GraphQL, permitindo:

- Cadastro de clientes;
- Processamento de eventos recebidos via webhook;
- Classificação automática de prioridade;
- Controle de idempotência de eventos;
- Persistência dos dados em PostgreSQL.

## Vídeo de devesa: <https://www.youtube.com/watch?v=dLPzmYnF4Kg>

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

## Swagger

A documentação da API está disponível em:

<http://localhost:8000/docs>

Caso o ambiente resolva `localhost` para IPv6 (`::1`) e ocorra falha de conexão, utilize:

<http://127.0.0.1:8000/docs>

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

# Visão de Produção AWS

Embora o desafio tenha sido desenvolvido utilizando Docker e PostgreSQL local, em um ambiente produtivo a arquitetura poderia ser escalada utilizando serviços gerenciados da AWS.

## Entrada das Requisições

Os endpoints da aplicação poderiam ser publicados através do **Amazon API Gateway**, responsável por receber as requisições HTTP externas, aplicar controle de acesso, monitoramento e limitação de tráfego.

## Camada de Aplicação

A API FastAPI poderia ser executada em containers utilizando **Amazon ECS Fargate**, eliminando a necessidade de gerenciamento de servidores. Dessa forma seria possível aumentar ou reduzir automaticamente a quantidade de instâncias da aplicação de acordo com a demanda.

Fluxo:

```text
Cliente
  ↓
API Gateway
  ↓
ECS Fargate (FastAPI)
```

## Banco de Dados

Os dados dos clientes e dos eventos processados seriam armazenados em um **Amazon RDS PostgreSQL**, mantendo compatibilidade com a implementação atual.

O RDS fornece:

- Backups automáticos;
- Replicação;
- Atualizações gerenciadas;
- Monitoramento integrado;
- Alta disponibilidade através de Multi-AZ.

Fluxo:

```text
FastAPI
   ↓
RDS PostgreSQL
```

## Processamento de Webhooks

Em cenários de alto volume, o endpoint de webhook poderia publicar os eventos em uma fila utilizando **Amazon SQS**.

Dessa forma a API responderia rapidamente ao Pipefy sem depender do processamento completo da regra de negócio.

Fluxo:

```text
Pipefy
   ↓
API Gateway
   ↓
FastAPI
   ↓
SQS
   ↓
Worker de Processamento
   ↓
RDS PostgreSQL
```

Essa abordagem reduz o risco de perda de eventos e melhora a capacidade de processamento em picos de carga.

## Logs e Monitoramento

Os logs da aplicação poderiam ser enviados para o **Amazon CloudWatch**, permitindo:

- Centralização dos logs;
- Métricas de utilização;
- Alarmes automáticos;
- Rastreamento de falhas.

## Gerenciamento de Credenciais

Informações sensíveis como credenciais do banco de dados e tokens de integração com o Pipefy poderiam ser armazenadas no **AWS Secrets Manager**, evitando exposição em arquivos de configuração ou imagens Docker.

## Escalabilidade

A arquitetura proposta permite:

- Escalabilidade horizontal da API através do ECS Fargate;
- Escalabilidade vertical e horizontal do banco via RDS;
- Processamento assíncrono dos webhooks através de filas;
- Alta disponibilidade com serviços gerenciados da AWS.

Essa abordagem mantém a mesma regra de negócio implementada no desafio, porém preparada para atender volumes significativamente maiores de clientes e eventos.

---

# Outras melhorias Futuras para produção

Em um ambiente produtivo seriam considerados:

- Alembic para versionamento de banco;
- Integração real com a API GraphQL do Pipefy;
- CI/CD;- Monitoramento e observabilidade.

---

# Autor

Israel Hamdan
