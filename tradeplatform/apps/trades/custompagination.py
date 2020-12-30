from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetPaginationWithUpperBound(LimitOffsetPagination):
    """Pagination class with max 8 instances per page."""

    max_limit = 5
