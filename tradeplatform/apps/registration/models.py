from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """Class that represent user's profile"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_valid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
