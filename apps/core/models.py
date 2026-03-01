from django.db import models
from apps.common.models import BaseModel
from django.conf import settings

class Project(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
