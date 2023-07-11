from copy import copy

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from activity.serializers import OrderSerializers


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializers
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = copy(request.data)
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

