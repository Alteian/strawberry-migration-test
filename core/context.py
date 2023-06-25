import typing

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from strawberry.django.context import StrawberryDjangoContext
from functools import cached_property
from graphql.error import GraphQLError

from core.shared.graphql.utils import jwt_decode_and_is_expired
from core.shared.graphql.exceptions import TokenExpiredException
from core.user.graphql.types import UserType

class Context(StrawberryDjangoContext):
    
    @cached_property
    def user(self) -> typing.Optional[UserType]:
        if not self.request:
            return None
        authorization = self.request.headers.get("Authorization", None)
        if not authorization:
            return AnonymousUser()
        try:
            decoded = jwt_decode_and_is_expired(authorization[7:])
            id = decoded.get("id", None)
            user = get_user_model().objects.get(id=id)
            return user
        except TokenExpiredException as e:
            raise GraphQLError(str(e))
        except get_user_model().DoesNotExist:
            raise GraphQLError(_("User not found"))
