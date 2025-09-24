from rest_framework.permissions import BasePermission, SAFE_METHODS


# This permission provides retrieving and updating rights for board members and the board owner and deleting rights for the board owner.
class IsBoardOwnerOrMember(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        return True  
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS or request.method == 'PATCH':
            return obj.owner == user or user in obj.members.all()
        elif request.method == 'DELETE':
            return obj.owner == user
        else:
            return False


# Object Permission when the user is member of the board.   
class IsBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        board = obj.board
        return board.members.filter(id=request.user.id).exists()


# The class `IsBoardOfTaskMember` defines permission checks when the user is member of the board where the task is assigned. It also defines deleting rights for comment authors.
class IsBoardOfTaskMember(BasePermission):
    def has_permission(self, request, view):
        task = view.get_task()
        if not task:
            return False
        if request.method in SAFE_METHODS or request.method == 'POST':
            return task.board.members.filter(id=request.user.id).exists()
        return request.method == 'DELETE'

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            return obj.author_id == request.user.id
        if request.method in SAFE_METHODS:
            return obj.task.board.members.filter(id=request.user.id).exists()
        return False


# Permission to retrieve tasks when user is assignee of the task.
class IsAssignee(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return bool(request.user == obj.assignee)
        return True


# Permission to retrieve tasks when user is reviewer of the task.
class IsReviewer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return bool(request.user == obj.reviewer)
        return True


# Class to define permission checks for different actions for a task. Updating rights are only given to users which are members of the board. Deleting rights are only for the creator of the task and the owner of the board.
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