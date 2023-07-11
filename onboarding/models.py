from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


def cac_directory_path(instance):
    return 'cac_{0}/{1}'.format(instance.name, instance.tone)


def compliance_directory_path(instance):
    return 'compliance_{0}/{1}'.format(instance.name, instance.tone)


class Business(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='user_businesses',
                             null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=255, blank=True, null=True)
    cac = models.FileField(upload_to=cac_directory_path, blank=True, null=True)
    compliance = models.FileField(upload_to=compliance_directory_path, blank=True, null=True)


class Product(TimeStampedModel):
    business = models.ForeignKey('onboarding.Business', on_delete=models.SET_NULL, related_name='businesses_product',
                             null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.CharField(max_length=255, blank=True, null=True)



