from django.urls import path

from apps.registration import views

urlpatterns = [
    path("activate/<token>/", views.ActivateUserEmail.as_view(), name="activate"),
]
