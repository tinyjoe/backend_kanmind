from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsBoardOwnerOrMember(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        return True  
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return obj.owner == user or user in obj.members.all()
        elif request.method == 'DELETE':
            return obj.owner == user
        else:
            return False
    
class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        board = obj.board
        return board.members.filter(id=request.user.id).exists()
    
class IsAssignee(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return bool(request.user == obj.assignee)
        return True
    
class IsReviewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return bool(request.user == obj.reviewer)
        return True
    
class IsAllowedToUpdateOrDelete(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'PATCH':
            return obj.board.members.filter(id=user.id).exists()
        elif request.method == 'DELETE':
            return (obj.creator == user) or (obj.board.owner == user)
        else:
            return False