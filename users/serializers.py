from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.services import UserService
from password_strength import PasswordPolicy


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    account_type = serializers.CharField(required=False)
    channel = serializers.CharField(required=False)
    fcmb_token = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    privacy = serializers.BooleanField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        privacy = attrs.get('privacy')

        if not email:
            raise serializers.ValidationError({"email": "Email is required"})
        if not password:
            raise serializers.ValidationError({"password": "Password is required"})
        if not privacy:
            raise serializers.ValidationError({"privacy": "You Must agree to our Privacy Terms"})

        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        account_type = validated_data.get('account_type')
        channel = validated_data.get('channel')
        fcmb_token = validated_data.get('fcmb_token')
        username = validated_data.get('username')
        user = UserService().create_user(
            email=email, password=password, account_type=account_type, channel=channel, fcmb_token=fcmb_token,
            username=username
        )
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    remember_me = serializers.BooleanField(default=False, write_only=True)
    device_name = serializers.CharField(max_length=255, allow_blank=False, required=True)
    device_id = serializers.CharField(max_length=255, allow_blank=False, required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    device_name = serializers.CharField(max_length=255, allow_blank=False, required=True)
    device_id = serializers.CharField(max_length=255, allow_blank=False, required=True)
    user = serializers.CurrentUserDefault()

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password does not match.")
        return value

    def validate_new_password(self, value):
        user = self.context["request"].user
        try:
            validate_password(value, user)
            policy = PasswordPolicy.from_names(
                lenght=8, uppercase=1, strength=0.3, entropybits=1, nonletterslc=1, numbers=1, symbols=1, special=1,
                nonletters=1
            )
            policy.test(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value


class SendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.EmailField()
    new_password = serializers.CharField(required=True)
