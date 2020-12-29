from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import viewsets

from django.contrib.auth.models import User
from apps.registration.models import UserProfile
from apps.registration.serializers import UserProfileSerializer, UserSerializer

from apps.registration.forms import SignupForm
from apps.registration.tokens import account_activation_token
from apps.registration.tasks import send_confirmation_mail_message


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User model"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for User Profile model"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


def signup(request):
    """View for user's registration"""

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            domain = get_current_site(request).domain

            send_confirmation_mail_message.delay(user_id=user.id, domain=domain)

            return HttpResponse(
                "Please confirm your email address to complete the registration"
            )
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})


def activate(request, uidb64, token):
    """View for confirmation user's mail address"""

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.profile.is_valid = True
        user.profile.save()
        login(request, user)
        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    else:
        return HttpResponse("Activation link is invalid!")
