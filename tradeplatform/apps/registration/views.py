from django.contrib.auth.models import User
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.registration.custompermission import IsOwnerOrReadOnly
from apps.registration.models import UserProfile
from apps.registration.serializers import (ConfirmResetPasswordSerializer,
                                           RequestResetPasswordSerializer,
                                           UserProfileSerializer,
                                           UserSerializer)
from apps.registration.services.views_logic import reset_user_password
from apps.registration.tasks import send_reset_password_mail
from apps.registration.tokens import confirm_user_email


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet for User Profile model"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    permission_classes = [IsOwnerOrReadOnly]


class SignUpView(generics.ListAPIView, generics.CreateAPIView):
    """View for user's registration"""

    serializer_class = UserSerializer

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """Function for getting information about view"""

        message = {"details": "Please write information below"}
        return Response(data=message, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Function for creating a request to reset user's password"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        message = {
            "details": "You are successfully registered. "
            "Please confirm your email address to complete the registration."
        }
        return Response(data=message, status=status.HTTP_201_CREATED, headers=headers)


class ActivateUserEmailView(generics.ListAPIView):
    """View for confirmation user's mail address"""

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """Return response to user with information about email confirmation"""

        if confirm_user_email(token=kwargs["token"]):
            message = {"details": "Thank you for your email confirmation."}
        else:
            message = {"details": "Invalid link!"}

        return Response(data=message, status=status.HTTP_200_OK)


class RequestResetPasswordView(generics.ListAPIView, generics.CreateAPIView):
    """View to request a password change"""

    serializer_class = RequestResetPasswordSerializer

    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Function for creating a request to reset user's password"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        send_reset_password_mail.delay(email=request.data["email"])

        message = {"details": "We send you confirmation mail for reset your password"}
        return Response(data=message, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """Function for getting information about view"""

        message = {"details": "Please write your email address to reset password"}
        return Response(data=message, status=status.HTTP_200_OK)


class ResetPasswordView(generics.ListAPIView, generics.CreateAPIView):
    """View for confirmation of changing user's password"""

    serializer_class = ConfirmResetPasswordSerializer

    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Function for changing user's password"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_user_password(token=kwargs["token"], password=request.data["password"])

        message = {"details": "Password has been successfully changed"}
        return Response(data=message, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """Function for getting information about view"""

        message = {"details": "Please write new password and confirm it"}
        return Response(data=message, status=status.HTTP_200_OK)
