from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    User can update only model instance that belongs to him
    But user can view all model instances and detail information about them
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user == obj.user