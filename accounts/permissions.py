from rest_framework.permissions import BasePermission, IsAuthenticated

class UnauthenticatedPost(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST']
