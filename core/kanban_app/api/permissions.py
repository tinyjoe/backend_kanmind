from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from kanban_app.models import Board

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
    
class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        board_id = request.data.get('board')
        try: 
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return False
        return board.members.filter(id=request.user.id).exists()