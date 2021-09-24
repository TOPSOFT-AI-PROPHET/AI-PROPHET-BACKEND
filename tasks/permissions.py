from rest_framework import permissions
from .models import AIModel
 
 
class IsOwnerOnly(permissions.BasePermission):
    """
    only the user can modify"""
    def has_permission(self, request, view):
        id = request.user.id
        AIM = AIModel.objects.get(ai_id=request.data["ai_id"])
        user_id = AIM.user_id
        if id != user_id:
            return False
        return True