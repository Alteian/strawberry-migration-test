from strawberry import Schema
from strawberry.tools import merge_types
from strawberry.schema.config import StrawberryConfig
from strawberry.extensions import QueryDepthLimiter
from strawberry_django_plus.directives import SchemaDirectiveExtension
from strawberry_django_plus.optimizer import DjangoOptimizerExtension

import strawberry

import core.user.graphql.schema

@strawberry.type
class PingQuery:
   @strawberry.field(description="A simple ping to test the server.")
   def ping(self) -> str:
       return "ping"

@strawberry.type
class PongQuery:
   @strawberry.field(description="A simple ping to test the server.")
   def pong(self) -> str:
       return "pong"

Query = merge_types(name="Query", types=(PingQuery, PongQuery, core.user.graphql.schema.UserQuery))

# Mutation = merge_types(name="Mutation", types=())

schema_extensions = [
    QueryDepthLimiter(max_depth=10), # TODO: find optimal amount.
    SchemaDirectiveExtension,
    DjangoOptimizerExtension,
    ]

schema = Schema(
    query=Query,
    #mutation=Mutation,
    config=StrawberryConfig(
        auto_camel_case=True,
        ),
    extensions=schema_extensions,
)