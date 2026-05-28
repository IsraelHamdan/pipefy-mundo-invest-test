from typing import TypedDict


class GraphQLPayload(TypedDict):
    query: str
    variables: dict