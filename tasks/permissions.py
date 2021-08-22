from rest_framework import permissions
from .models import AIModel
 
 
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    self-create permission, only the author can modify"""
    def has_permission(self, request, view):
        id = request.data['ai_id']
        AIM = AIModel.objects.get(ai_id=id)
        if AIM.user_id != request.user:
            return False
        return True