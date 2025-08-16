from rest_framework.permissions import BasePermission

class IsStudentOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and not hasattr(user, 'profile'):
            if user.is_authenticated and user.is_staff:
                return True
        else:
            return user.is_authenticated and user.profile.role == 'student' and user.student.status == 'activated'