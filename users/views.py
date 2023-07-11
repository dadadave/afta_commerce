from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import AuthTokenSerializer, SendResetPasswordEmailSerializer, ResetPasswordSerializer, \
    SignupSerializer
from users.services import AuthenticationService


class LoginView(ObtainAuthToken):
    """
        import requests

        data = {
            "email": "user@example.com",
            "password": "password",
            "remember_me": True,
            "device_name":"Windows",
            "device_id":"12345"
        }
        headers = {
            "Device-Name": "Windows",
            "Device-Id":"12345"
        }
        response = requests.post('http://localhost:8000/login/', json=data, headers=headers)

    """
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        device_name = request.headers.get("Device-Name", None)
        device_id = request.headers.get("Device-Id", None)
        request.data.update({"device_name": device_name, "device_id": device_id})
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        remember_me = serializer.validated_data.get('remember_me', False)
        device_name = serializer.validated_data.get('device_name', None)
        device_id = serializer.validated_data.get('device_id', None)
        token, created = Token.objects.get_or_create(user=user)
        user.logged_devices.create(device_name=device_name, device_id=device_id, token=token)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'device_name': device_name,
        })


class ResetPasswordEmailAPIView(GenericAPIView):
    serializer_class = SendResetPasswordEmailSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthenticationService.setup_reset_password(**serializer.validated_data)

        return Response(
            {"message": "Please, Check your mail."}, status=status.HTTP_200_OK
        )


class PasswordResetView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def get(self, request, token):
        if AuthenticationService.check_reset_token(token):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if AuthenticationService.reset_password(**serializer.validated_data):
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Remove the device from the user's logged_devices list
        device_name = request.headers.get("Device-Name")
        device_id = request.headers.get("Device-Id")
        device = request.user.logged_devices.filter(device_name=device_name, device_id=device_id).first()
        if device:
            device.delete()
            return Response({"message": "Device successfully logged out."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Device not found."}, status=status.HTTP_404_NOT_FOUND)


class CreateUserView(CreateAPIView):
    serializer_class = SignupSerializer