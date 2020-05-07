from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    """
    Object-level permission to only allow creators of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user
