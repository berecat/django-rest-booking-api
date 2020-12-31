from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.registration.models import UserProfile
from apps.registration.serializers import UserProfileSerializer, UserSerializer
from apps.trades.services.db_interaction import change_user_profile_valid_by_id
from apps.registration.tokens import check_token


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for User Profile model"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class ActivateUserEmail(APIView):
    """View for confirmation user's mail address"""

    def get(self, request, token):

        if check_token(token=token):
            change_user_profile_valid_by_id(user_id=request.user)
            message = {"details": "Thank you for your email confirmation. Now you can login your account."}
        else:
            message = {"details": "Invalid link!"}

        return Response(data=message)


