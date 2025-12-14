from rest_framework import permissions # type: ignore

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to anyone,
    but write access only to admin users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
