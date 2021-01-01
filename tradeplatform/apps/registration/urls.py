from django.urls import path

from apps.registration import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("activate/<token>/", views.ActivateUserEmailView.as_view(), name="activate"),
    path("reset_password/", views.RequestResetPasswordView.as_view(), name="reset"),
    path(
        "reset_password/<token>/",
        views.ResetPasswordView.as_view(),
        name="confirm_reset",
    ),
    path(
        "change_email/",
        views.RequestChangeEmailAddressView.as_view(),
        name="request_change_email",
    ),
    path(
        "change_email/<token>/",
        views.ChangeEmailAddressView.as_view(),
        name="change_email",
    ),
    path(
        "change_email/confirm/<token>/",
        views.ActivateUserEmailView.as_view(),
        name="confirm_change_email",
    ),
]
