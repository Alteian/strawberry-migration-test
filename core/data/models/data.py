import uuid

from django.db import models


from core.shared.models import BaseModel
from core.user.models import User



class Data(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="data",
        null=True,
        blank=True,
    )
    long_text = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Data"
        verbose_name_plural = "Data"
