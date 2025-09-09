from django.contrib.auth.models import User
from rest_framework import serializers
from kanban_app.models import Board, BoardTask, TaskComment
from .validators import validate_board_member, validate_user_in_board

class BoardListSerializer(serializers.ModelSerializer):
    members = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    class Meta: 
        model= Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members']

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        # TODO: Anpassen, wenn Tickets ins Modell kommen
        return 0

    def get_tasks_to_do_count(self, obj):
        # TODO: Anpassen
        return 0

    def get_tasks_high_prio_count(self, obj):
        # TODO: Anpassen
        return 0

class UserNestedSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'email', 'username']


class TaskListSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="assignee", write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="reviewer", write_only=True, required=False, allow_null=True)
    assignee = UserNestedSerializer(read_only=True)
    reviewer = UserNestedSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    class Meta: 
        model = BoardTask
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date', 'comments_count', 'assignee', 'reviewer']

    def validate(self, data):
        board = data.get("board")
        user = self.context["request"].user
        validate_board_member(board, user)
        assignee = data.get("assignee")
        reviewer = data.get("reviewer")
        if assignee:
            validate_user_in_board(board, assignee.id, "Assignee")
        if reviewer:
            validate_user_in_board(board, reviewer.id, "Reviewer")
        return data

    def get_comments_count(self, obj):
        return 0

class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserNestedSerializer(many=True)
    tasks = serializers.PrimaryKeyRelatedField(queryset=BoardTask.objects.all(), many=True)
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
