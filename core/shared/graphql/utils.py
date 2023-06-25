import jwt
import time
import os
import strawberry
import typing

from strawberry.types import Info
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

from .constants import PRIVATE_KEY, PUBLIC_KEY
from .exceptions import TokenExpiredException


env_private_key_bytes = os.getenv('PRIVATE_KEY', default=PRIVATE_KEY).replace('\\n', '\n').encode()
env_public_key_bytes = os.getenv('PUBLIC_KEY', default=PUBLIC_KEY).replace('\\n', '\n').encode()
private_key = load_pem_private_key(env_private_key_bytes, password=None, backend=default_backend())
public_key = load_pem_public_key(env_public_key_bytes, backend=default_backend())

def jwt_decode_and_is_expired(token):
    """
    Pass encoded token to receive decoded token and verify expiration.
    """
    # with options verify_exp=True, we get generic error message "Signature has expired"
    # I have changed it to boolean operation to get more specific result for frontend
    jwt_token = jwt.decode(token, key=public_key, algorithms=["EdDSA"], options={"verify_exp": False})
    if jwt_token['exp'] <= int(time.time()):
        raise TokenExpiredException("Token expired.")
    elif jwt_token['exp'] > int(time.time()):
        return jwt_token

from core.user.graphql.types import UserType
from django.db import models
@strawberry.type
class CustomuserConnection(strawberry.relay.Connection[UserType]):
    @classmethod
    def resolve_connection(
        cls,
        nodes: typing.Iterable[UserType],
        *,
        info: Info,
        before: typing.Optional[str] = None,
        after: typing.Optional[str] = None,
        first: typing.Optional[int] = None,
        last: typing.Optional[int] = None,
    ):
        edges_mapping = {
            strawberry.relay.to_base64("user", n.id): strawberry.relay.Edge(
                node=n,
                cursor=strawberry.relay.to_base64("user", n.first_name),
            )
            for n in sorted(nodes, key=lambda f: f.first_name)
        }
        edges = list(edges_mapping.values())
        first_edge = edges[0] if edges else None
        last_edge = edges[-1] if edges else None
        if after is not None:
            after_edge_idx = edges.index(edges_mapping[after])
            edges = [e for e in edges if edges.index(e) > after_edge_idx]
        if before is not None:
            before_edge_idx = edges.index(edges_mapping[before])
            edges = [e for e in edges if edges.index(e) < before_edge_idx]
        if first is not None:
            edges = edges[:first]
        if last is not None:
            edges = edges[-last:]
        return cls(
            edges=edges,
            page_info=strawberry.relay.PageInfo(
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if edges else None,
                has_previous_page=(
                    first_edge is not None and bool(edges) and edges[0] != first_edge
                ),
                has_next_page=(
                    last_edge is not None and bool(edges) and edges[-1] != last_edge
                ),
            ),
        )

from strawberry_django_plus import gql

from strawberry_django_plus.relay import ListConnectionWithTotalCount
from django.db.models import QuerySet

@strawberry.type
class CustomSeconduserConnection(strawberry.relay.Connection[UserType]):
    @classmethod
    def resolve_connection(
        cls,
        nodes: typing.Iterable[UserType],
        *,
        info: Info,
        before: typing.Optional[str] = None,
        after: typing.Optional[str] = None,
        first: typing.Optional[int] = None,
        last: typing.Optional[int] = None,
    ):
        edges_mapping = {
            strawberry.relay.to_base64("user", n.id): strawberry.relay.Edge(
                node=n,
                cursor=strawberry.relay.to_base64("user", n.first_name),
            )
            for n in sorted(nodes, key=lambda f: f.first_name)
        }
        edges = list(edges_mapping.values())
        first_edge = edges[0] if edges else None
        last_edge = edges[-1] if edges else None
        if after is not None:
            after_edge = edges_mapping.get(after)
            if after_edge:
                after_edge_idx = edges.index(after_edge)
                edges = [e for index, e in enumerate(edges) if index > after_edge_idx]
        if before is not None:
            before_edge = edges_mapping.get(before)
            if before_edge:
                before_edge_idx = edges.index(before_edge)
                edges = [e for index, e in enumerate(edges) if index < before_edge_idx]
        if first is not None:
            edges = edges[:first]
        if last is not None:
            edges = edges[-last:]
        return cls(
            edges=edges,
            page_info=strawberry.relay.PageInfo(
                start_cursor=edges[0].cursor if edges else None,
                end_cursor=edges[-1].cursor if edges else None,
                has_previous_page=(
                    first_edge is not None and bool(edges) and edges[0] != first_edge
                ),
                has_next_page=(
                    last_edge is not None and bool(edges) and edges[-1] != last_edge
                ),
            ),
        )
from django.db import connection

@strawberry.type
class CustomUserRelayConnection(ListConnectionWithTotalCount[strawberry.relay.NodeType]):
    @gql.field
    def total_count(self) -> typing.Optional[int]:
        """Total quantity of existing nodes."""
        assert self.nodes is not None
        total_count = None
        try:
            total_count = typing.cast("models.QuerySet[models.Model]", self.nodes).count()
            print(total_count.explain())
            print("AHA")
        except (AttributeError, ValueError, TypeError):
            if isinstance(self.nodes, typing.Sized):
                total_count = len(self.nodes)
                print("len aha")
        return total_count
    