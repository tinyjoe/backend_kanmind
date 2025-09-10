from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from kanban_app.models import Board, BoardTask

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
    def has_permission(self, request, view):
        board_id = request.data.get('board')
        try: 
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return False
        return bool(board.members.filter(id=request.user.id).exists())
    
class IsTaskReviewer(BasePermission):
    def has_permission(self, request, view):
        task_id = request.data.get('task')
        try: 
            task = BoardTask.objects.get(id=task_id)
        except BoardTask.DoesNotExist:
            return False
        return bool(request.user == task.reviewer)
    
class IsTaskAssignee(BasePermission):
    def has_permission(self, request, view):
        task_id = request.data.get('task')
        try: 
            task = BoardTask.objects.get(id=task_id)
        except BoardTask.DoesNotExist:
            return False
        if request.method == 'GET':
            return bool(request.user == task.reviewer)
        else:
            return False