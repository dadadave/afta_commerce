from rest_framework.serializers import ModelSerializer

from activity.models import Order


class OrderSerializers(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'user', 'business',
            'created_at', 'total_amount',
            'fulfilled', 'product', 'quantity'
        ]