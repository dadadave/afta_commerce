from django.urls import include, path
from rest_framework import routers

from activity.views import OrderViewSet

router = routers.DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]