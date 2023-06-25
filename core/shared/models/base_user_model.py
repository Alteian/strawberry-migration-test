from django.contrib.auth.base_user import AbstractBaseUser

from .base_model import BaseModel


class BaseUserModel(AbstractBaseUser, BaseModel):
    class Meta:
        abstract = True
