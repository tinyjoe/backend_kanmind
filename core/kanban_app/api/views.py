from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from .serializers import BoardListSerializer, TaskListSerializer, BoardDetailSerializer, UserNestedSerializer, TaskDetailSerializer
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