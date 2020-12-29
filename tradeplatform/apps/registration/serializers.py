from django.contrib.auth.models import User
from rest_framework import serializers

from apps.registration.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User Profile model"""

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = UserProfile
        fields = ("user", "is_valid", "date_joined")


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "profile")
