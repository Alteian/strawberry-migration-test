import uuid
import strawberry
from strawberry_django_plus import gql

from core.user.models import User

@gql.django.type(User)
class UserType(strawberry.relay.Node):
    id: strawberry.relay.NodeID[uuid.UUID]
    first_name: gql.auto
    last_name: gql.auto
    email: gql.auto
    @gql.field
    def mode(self, info) -> str:
        return self._mode