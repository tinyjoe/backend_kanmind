from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, viewsets, generics
from rest_framework.permissions import IsAuthenticated

from .serializers import BoardSerializer
from kanban_app.models import Board, BoardTask, TaskComment
from .permissions import IsBoardOwnerOrMember

class BoardsView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def post(self, request, *args, **kwargs):
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