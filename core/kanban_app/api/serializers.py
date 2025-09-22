from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import serializers

from kanban_app.models import Board, BoardTask, TaskComment
from .validators import validate_board_member, validate_user_in_board


# This class is a nested serializer for the User model in Django, including a custom method to retrieve the user's full name.
class UserNestedSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta: 
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.username


# This class is a nested serializer for the User model that includes a SerializerMethodField for the fullname field to show only the full name of a user in the comment.
class AuthorNestedSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta: 
        model = User
        fields = ['fullname']

    def get_fullname(self, obj):
        return obj.username


class TaskCommentSerializer(serializers.ModelSerializer):
    author = author = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = TaskComment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError('Content darf nicht leer sein.')
        return value


class TaskListSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='reviewer', write_only=True, required=False, allow_null=True)
    assignee = UserNestedSerializer(read_only=True)
    reviewer = UserNestedSerializer(read_only=True)
    comments = TaskCommentSerializer
    comments_count = serializers.SerializerMethodField()
    class Meta: 
        model = BoardTask
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'assignee', 'reviewer', 'due_date', 'comments_count']

    def validate(self, data):
        board = data.get('board')
        user = self.context['request'].user
        validate_board_member(board, user)
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')
        if assignee:
            validate_user_in_board(board, assignee.id, 'Assignee')
        if reviewer:
            validate_user_in_board(board, reviewer.id, 'Reviewer')
        return data
    
    def get_comments_count(self, obj):
        return obj.comments.count()

class TaskDetailSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='reviewer', write_only=True, required=False, allow_null=True)
    assignee = UserNestedSerializer(read_only=True)
    reviewer = UserNestedSerializer(read_only=True)

    class Meta:
        model = BoardTask
        fields = ['id', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date', 'assignee', 'reviewer']
        read_only_fields = ['creator', 'board']

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
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        to_do_tasks = obj.tasks.filter(Q(status='todo'))
        return to_do_tasks.count()

    def get_tasks_high_prio_count(self, obj):
        high_prio_tasks = obj.tasks.filter(Q(priority='high'))
        return high_prio_tasks.count()

class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserNestedSerializer(many=True, read_only=True)
    tasks = TaskListSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']
