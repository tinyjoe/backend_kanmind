from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import BoardListSerializer, TaskListSerializer, BoardDetailSerializer, UserNestedSerializer, TaskDetailSerializer, TaskCommentSerializer, BoardDetailUpdateSerializer
from kanban_app.models import Board, BoardTask, TaskComment
from .permissions import IsBoardOwnerOrMember, IsBoardMember, IsAllowedToUpdateOrDelete, IsAssignee, IsReviewer, IsBoardOfTaskMember
from .validators import validate_email_address
from .services import get_user_by_email


"""
The `BoardsView` class defines a view for listing and creating Board objects, with permission checks for authenticated users who are either the owner or a member of a board.
"""
class BoardsView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            members_ids = serializer.validated_data.pop("members", [])
            user = request.user
            board = Board.objects.create(owner=user, title=serializer.validated_data["title"])
            if members_ids:
                board.members.add(*members_ids)
            read_serializer = self.get_serializer(board)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

"""
This is a view for retrieving, updating, and deleting a Board object with different serializer classes based on the request method. For retrieving and updating are two different responses provided. These requests can only be performed if the user is the owner or one of the members of the board.
"""
class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return BoardDetailUpdateSerializer
        return BoardDetailSerializer
        

"""
This class represents a view in a Django REST framework API for listing and creating BoardTask objects with authentication and permission checks.
"""
class TaskListView(generics.ListCreateAPIView):
    queryset = BoardTask.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        return BoardTask.objects.all()
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        board_id = self.request.data.get('board')
        board = get_object_or_404(Board, pk=board_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(board=board, creator = request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
"""
This class represents a view for listing tasks that have the logged in user as the reviewer.
"""
class TaskReviewingListView(generics.ListAPIView):
    queryset = BoardTask.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsReviewer]

    def get_queryset(self):
        user = self.request.user
        return BoardTask.objects.filter(Q(reviewer=user))
    

"""
This class represents a view for listing tasks that have the logged in user as the assignee.
"""
class AssignedTaskListView(generics.ListAPIView):
    queryset = BoardTask.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsAssignee]

    def get_queryset(self):
        user = self.request.user
        return BoardTask.objects.filter(Q(assignee=user))
    
    
"""
A view to check if a specific mail address can be found in the user data to check if the user of this mail address can be added to a board as a member.
"""
class CheckEmailView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        email = request.query_params.get("email")
        error_response = validate_email_address(email)
        if error_response:
            return error_response
        user = get_user_by_email(email)
        if isinstance(user, Response):
            return user
        serializer = UserNestedSerializer(user)
        return Response(serializer.data)


"""
This is a view for retrieving, updating and deleting tasks of a specific board. The permissions requires the logged in user to be member of the board for updating the task and to be creator or board owner for deleting the task.
"""
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardTask.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated, IsAllowedToUpdateOrDelete]


"""
The `TaskCommentMixin` class provides methods to retrieve a task and check if the current user is a member of the board associated with that task.
"""
class TaskCommentMixin:
    def get_task(self):
        task_id = self.kwargs.get('task_id')
        return get_object_or_404(BoardTask, pk=task_id)

    def check_board_membership(self):
        task = self.get_task()
        if not task.board.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied('You have to be a member of the board.')
        

"""
This class represents a view for listing and creating task comments with permissions for board members and a filter method to get the comments of a specific task.
"""
class TaskCommentListView(TaskCommentMixin, generics.ListCreateAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated, IsBoardOfTaskMember]

    def get_queryset(self):
        return TaskComment.objects.filter(task=self.get_task())

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response({'error': 'Body must not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(task=self.get_task(), author=self.request.user)
            


"""
The class `TaskCommentDeleteView` allows users who are board members of a task to delete their own comments.
"""
class TaskCommentDeleteView(TaskCommentMixin, generics.DestroyAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated, IsBoardOfTaskMember]

    def get_object(self):
        return get_object_or_404(TaskComment, pk=self.kwargs['comment_id'], task=self.get_task())

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Only the author of the comment can delete.')
        instance.delete()