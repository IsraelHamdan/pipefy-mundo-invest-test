from app.enuns.client_enuns import Prioridade, Status
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


    def build_update_fields_values_mutation(
        self,
        card_id: str,
        prioridade: Prioridade
    ) -> GraphQLPayload:

        query = """
            mutation UpdateFieldsValues(
            $input: UpdateFieldsValuesInput!
            ) {
                updateFieldsValues(
                    input: $input
                ) {
                    success
                }
        }
        """

        variables = {
            "input": {
                "nodeId": card_id,
                "values": [
                    {
                        "fieldId": "status",
                        "value": Status.PROCESSADO.value
                    },
                    {
                        "fieldId": "prioridade",
                        "value": prioridade.value
                    }
                ]
            }
        }
        return {
            "query": query,
            "variables": variables
        }
