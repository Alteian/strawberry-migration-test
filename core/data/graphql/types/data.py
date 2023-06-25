import typing
import uuid
import strawberry
from strawberry_django_plus import gql

from core.data.models import Data
from core.user.graphql.types import UserType


@gql.django.type(Data)
class DataType(strawberry.relay.Node):
    id: strawberry.relay.NodeID[uuid.UUID]
    name: gql.auto
    description: gql.auto
    url: gql.auto
    user: typing.Optional[UserType]
    long_text: gql.auto
