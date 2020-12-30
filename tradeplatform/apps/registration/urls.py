from django.urls import path

from apps.registration import views

urlpatterns = [
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
]
