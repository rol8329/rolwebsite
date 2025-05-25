# account/permissions.py
from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission to check user roles.
    - reader: can only read
    - creator: can read and create
    - owner: can read, create, update, delete
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user_role = request.user.role

        # Owner can do everything
        if user_role == 'owner':
            return True

        # Creator can read and create
        if user_role == 'creator':
            return request.method in ['GET', 'POST', 'HEAD', 'OPTIONS']

        # Reader can only read
        if user_role == 'reader':
            return request.method in ['GET', 'HEAD', 'OPTIONS']

        return False

    def has_object_permission(self, request, view, obj):
        user_role = request.user.role

        # Owner can do everything
        if user_role == 'owner':
            return True

        # Creator can read and update their own objects
        if user_role == 'creator':
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True
            # Check if user owns the object
            if hasattr(obj, 'author') and obj.author == request.user:
                return request.method in ['PUT', 'PATCH', 'DELETE']
            return False

        # Reader can only read
        if user_role == 'reader':
            return request.method in ['GET', 'HEAD', 'OPTIONS']

        return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only to the owner
        return obj.author == request.user