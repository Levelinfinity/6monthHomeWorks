from rest_framework.permissions import BasePermission


class IsAdminOnly(BasePermission):
    """
    Только пользователи с ролью администратора.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'ADMIN'
        )



class IsUserOnly(BasePermission):
    """
    Только пользователи с ролью пользователя.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'USER'
        )