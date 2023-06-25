import strawberry
import typing

from strawberry.types import Info
from strawberry_django_plus import gql

from core.shared.graphql.utils import CustomuserConnection, CustomSeconduserConnection, CustomUserRelayConnection
from core.user.models import User
from django.db.models import Value
from django.db.models.functions import Cast
from django.db.models import CharField
from core.user.graphql.types import UserType
from strawberry_django_plus.optimizer import optimize

@strawberry.type
class UserQuery:
    @strawberry.relay.connection(CustomuserConnection)
    def user_connection(
        self,
        info: Info,
    ) -> typing.Iterable[User]:
        return User.objects.all()
    
    @strawberry.relay.connection(CustomUserRelayConnection[UserType])
    def second_connection(
        self,
        info: Info,
    ) -> typing.Iterable[User]:
        users = optimize(User.objects.all().annotate(_mode=Value("my_user", output_field=CharField())), info)
        return users


