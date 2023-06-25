import strawberry
import typing

from strawberry.types import Info
from strawberry_django_plus import gql

from core.shared.graphql.utils import CustomuserConnection, CustomSeconduserConnection
from core.user.models import User

@strawberry.type
class UserQuery:
    @strawberry.relay.connection(CustomuserConnection)
    def user_connection(
        self,
        info: Info,
    ) -> typing.Iterable[User]:
        return User.objects.all()
    
    @strawberry.relay.connection(CustomSeconduserConnection)
    def second_connection(
        self,
        info: Info,
    ) -> typing.Iterable[User]:
        return User.objects.all()


