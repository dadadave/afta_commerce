import uuid as uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser


class User(TimeStampedModel, AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='user_parent')
    account_type = models.CharField(max_length=255, blank=True, null=True)
    channel = models.CharField(max_length=255, blank=True, null=True)
    fcmb_token = models.CharField(max_length=255, blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class ResetToken(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reset_token')
    token = models.CharField(max_length=255, blank=True, null=True)