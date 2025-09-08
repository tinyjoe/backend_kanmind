from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

class IsBoardOwnerOrMember(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user and request.user.is_authenticated
        return True  
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            user = request.user
            return obj.owner == user or user in obj.members.all()
        return True