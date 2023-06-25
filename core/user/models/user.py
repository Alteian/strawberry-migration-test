import uuid
import typing

from django.db import models
from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager

from core.shared.models import BaseUserModel


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        model: str = None,
        **kwargs: typing.Any,
    ) -> object:
        if not model:
            model = self.model
        user = model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str, first_name: str, last_name: str
    ) -> object:
        user = self.create_user(
            email,
            password=password,
            model=apps.get_model("core.user", "User"),
        )
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_email(self, email: str) -> object:
        return self.get_queryset().get(email=email.lower())

    def get_by_natural_key(self, email: str) -> object:
        return self.get(**{self.model.EMAIL_FIELD + "__iexact": email})




class User(BaseUserModel):
    USERNAME_FIELD = EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    objects = UserManager()

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="general-user-User-id-label",
    )
    first_name = models.CharField(
        max_length=255, verbose_name="general-user-User-first_name-label"
    )
    last_name = models.CharField(
        max_length=255, verbose_name="general-user-User-last_name-label"
    )
    email = models.EmailField(
        unique=True, verbose_name="general-user-User-email-label"
    )

    is_staff = models.BooleanField(
        default=False,
    )
    is_superuser = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "general-user-User-label"
        verbose_name_plural = "general-user-Users-label"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"