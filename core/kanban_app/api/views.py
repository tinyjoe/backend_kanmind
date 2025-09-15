from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied

from .serializers import BoardListSerializer, TaskListSerializer, BoardDetailSerializer, UserNestedSerializer, TaskDetailSerializer, TaskCommentSerializer
from kanban_app.models import Board, BoardTask, TaskComment
from .permissions import IsBoardOwnerOrMember, IsBoardMember, IsAllowedToUpdateOrDelete
from .validators import validate_email_address
from .services import get_user_by_email

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
            return Response(read_serializer.data)
        else:
            return Response(serializer.errors)
        

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
        

class TaskListView(generics.ListCreateAPIView):
    queryset = BoardTask.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        return BoardTask.objects.all()
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(creator = request.user)
        return Response(serializer.data)
    
class TaskReviewingListView(generics.ListAPIView):
    queryset = BoardTask.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BoardTask.objects.filter(Q(reviewer=user))
    

class AssignedTaskListView(generics.ListAPIView):
    queryset = BoardTask.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BoardTask.objects.filter(Q(assignee=user))
    

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
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BoardTask.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAuthenticated, IsAllowedToUpdateOrDelete]


class TaskCommentMixin:
    def get_task(self):
        task_id = self.kwargs.get('task_id')
        return get_object_or_404(BoardTask, pk=task_id)

    def check_board_membership(self):
        task = self.get_task()
        if not task.board.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied('You have to be a member of the board.')
        
class TaskCommentListView(TaskCommentMixin, generics.ListCreateAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        return TaskComment.objects.filter(task=self.get_task())

    def perform_create(self, serializer):
        self.check_board_membership()
        serializer.save(task=self.get_task(), author=self.request.user)


class TaskCommentDeleteView(TaskCommentMixin, generics.DestroyAPIView):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_object(self):
        self.check_board_membership()
        return get_object_or_404(TaskComment, pk=self.kwargs['comment_id'], task=self.get_task())

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Only the author of the comment can delete.')
        instance.delete()