from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .serializers import BoardListSerializer, TaskListSerializer, BoardDetailSerializer
from kanban_app.models import Board, BoardTask, TaskComment
from .permissions import IsBoardOwnerOrMember, IsBoardMember

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
        board = self.request.board
        return BoardTask.objects.filter(Q(board=board)).distinct()
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            self.perform_create(serializer)
        return Response(serializer.data)