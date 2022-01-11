from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # edit permissions are only allowed to the author
        return obj.user == request.user 
