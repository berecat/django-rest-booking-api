from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.registration.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User Profile model"""

    user = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "user",
            "is_valid",
            "date_joined",
        )
        read_only_fields = ("is_valid",)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "password2",
            "profile",
        )

    def validate(self, attrs):
        """Check that password fields match"""

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        """Method for creating user instance"""

        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class RequestResetPasswordSerializer(serializers.Serializer):
    """Serializer for creating a request to change user's password"""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """Check that user, which have the given email, exist"""

        if not User.objects.all().filter(email=attrs["email"]):
            raise serializers.ValidationError(
                {"email": "User with the given email address does not exist."}
            )

        return attrs


class ConfirmResetPasswordSerializer(serializers.Serializer):
    """Serializer for confirmation changing user's password"""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        """Check that password fields match"""

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs
