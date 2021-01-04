from django_filters import DateTimeFilter, FilterSet

from apps.registration.models import UserProfile


class UserProfileFilter(FilterSet):
    """Filter class for Price model"""

    from_date_joined = DateTimeFilter(field_name="date_joined", lookup_expr="gte")
    to_date_joined = DateTimeFilter(field_name="date_joined", lookup_expr="lte")

    class Meta:
        model = UserProfile
        fields = (
            "user__username",
            "user__email",
            "from_date_joined",
            "date_joined",
            "to_date_joined",
            "is_valid",
        )
