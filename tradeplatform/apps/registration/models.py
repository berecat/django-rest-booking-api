from django.db import models


class UserProfile(models.Model):
    """Class that represent user's profile"""

    is_valid = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
