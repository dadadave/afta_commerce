from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_orders',
                             null=True, blank=True)
    business = models.ForeignKey('onboarding.Business', on_delete=models.SET_NULL, related_name='businesses_orders',
                                 null=True, blank=True)
    product = models.ForeignKey('onboarding.Product', on_delete=models.SET_NULL, related_name='product_orders',
                                 null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    quantity = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fulfilled = models.BooleanField(default=False)

    # Add any additional fields as per your requirements

    def total_amount_cal(self):
        total_amount = float(self.product.price) * int(self.quantity)
        return total_amount

    def __str__(self):
        return f"Order #{self.id}"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.total_amount = self.total_amount_cal()
        return super().save()
