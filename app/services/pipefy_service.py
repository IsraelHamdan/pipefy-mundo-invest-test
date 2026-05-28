from app.models.client import Client
from app.schema.client_schema import CreateClientDTO

from app.types.graphql import GraphQLPayload

from app.core.config import settings


class PipefyService:

    def build_create_card_mutation(
        self,
        data: CreateClientDTO
    ) -> GraphQLPayload:

        query = """
        mutation CreateCard($input: CreateCardInput!) {
          createCard(input: $input) {
            card {
              id
              title
            }
          }
        }
        """

        variables = {
            "input": {
                "pipe_id": settings.PIPEFY_PIPE_ID,

                "title": data.cliente_nome,

                "fields_attributes": [
                    {
                        "field_id": "cliente_nome",
                        "field_value": data.cliente_nome
                    },
                    {
                        "field_id": "cliente_email",
                        "field_value": data.cliente_email
                    },
                    {
                        "field_id": "tipo_solicitacao",
                        "field_value": data.tipo_solicitacao
                    },
                    {
                        "field_id": "valor_patrimonio",
                        "field_value": str(data.valor_patrimonio)
                    }
                ]
            }
        }

        return {
            "query": query,
            "variables": variables
        }


    def build_update_card_mutation(
        self,
        card_id: str,
        priority: str
    ):

        query = """
        mutation UpdateCardField(
            $card_id: ID!,
            $field_id: String!,
            $new_value: String!
        ) {
        updateCardField(
            input: {
            card_id: $card_id
            field_id: $field_id
            new_value: $new_value
            }
        ) {
            card {
            id
            }
        }
        }
        """

        variables = {
            "card_id": card_id,
            "field_id": "prioridade",
            "new_value": priority
        }

        return {
            "query": query,
            "variables": variables
        }