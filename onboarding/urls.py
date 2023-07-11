from django.urls import path, include
from rest_framework import routers

from onboarding.views import BusinessProductViewSet, BusinessViewSet

router = routers.DefaultRouter()
router.register(r'business', BusinessViewSet, basename='business')
router.register(r'product', BusinessProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls)),
]
