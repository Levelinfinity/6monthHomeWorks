from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTeacherOrReadOnly(BasePermission):
    """
    GET, HEAD, OPTIONS — разрешены любым авторизованным пользователям.
    POST, PUT, PATCH, DELETE — только пользователям с ролью 'teacher'[cite: 1].
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in SAFE_METHODS:
            return True
            
        return getattr(request.user, 'role', None) == 'teacher'