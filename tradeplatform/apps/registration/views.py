from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import viewsets

from apps.registration.models import UserProfile
from apps.registration.serializers import UserProfileSerializer, UserSerializer
from apps.registration.tasks import send_confirmation_mail_message
from apps.registration.tokens import account_activation_token
from apps.trades.services.db_interaction import (
    change_user_profile_valid_by_id, get_user_by_id)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        """"""

        send_confirmation_mail_message.delay(
            user_id=self.request.user.id, domain=get_current_site(self.request).domain
        )
        serializer.save()


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for User Profile model"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


def activate(request, uidb64, token):
    """View for confirmation user's mail address"""

    uid = force_text(urlsafe_base64_decode(uidb64))
    try:
        user = get_user_by_id(user_id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        change_user_profile_valid_by_id(user_id=uid)
        login(request, user)
        success_status = True
    else:
        success_status = False

    return render(
        request,
        "registration/register_confirm.html",
        {"success_status": success_status},
    )
