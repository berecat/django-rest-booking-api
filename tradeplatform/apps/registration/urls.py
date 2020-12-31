from django.urls import path

from apps.registration import views

urlpatterns = [
    path("activate/<token>/", views.ActivateUserEmailView.as_view(), name="activate"),
    path("reset_password/", views.RequestResetPasswordView.as_view(), name="reset"),
    path(
        "reset_password/<token>/",
        views.ResetPasswordView.as_view(),
        name="confirm_reset",
    ),
]
