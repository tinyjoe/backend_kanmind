from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import serializers

from kanban_app.models import Board, BoardTask, TaskComment
from .validators import validate_board_member, validate_board_user_relation


"""
This class is a nested serializer for the User model in Django, including a custom method to retrieve the user's full name.
"""
class UserNestedSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta: 
        model = User
        fields = ['id', 'email', 'fullname']

    def get_fullname(self, obj):
        return obj.username


"""
This class is a nested serializer for the User model that includes a SerializerMethodField for the fullname field to show only the full name of a user in the comment.
"""
class AuthorNestedSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta: 
        model = User
        fields = ['fullname']

    def get_fullname(self, obj):
        return obj.username


"""
The `TaskCommentSerializer` class defines a serializer for task comments with fields for id, creation date, author, and content, along with validation for the content field that must not be empty.
"""
class TaskCommentSerializer(serializers.ModelSerializer):
    author = author = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = TaskComment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['id', 'created_at', 'author']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError('The content must not be empty')
        return value


"""
The `TaskListSerializer` class serializes task data including assignee, reviewer, and comments count, with validation for board members and users.
"""
class TaskListSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='reviewer', write_only=True, required=False, allow_null=True)
    assignee = UserNestedSerializer(read_only=True)
    reviewer = UserNestedSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    class Meta: 
        model = BoardTask
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'assignee', 'reviewer', 'due_date', 'comments_count']

    def validate(self, data):
        board = data.get('board')
        user = self.context['request'].user
        assignee = data.get('assignee')
        reviewer = data.get('reviewer')
        validate_board_member(board, user)
        validate_board_user_relation(board, assignee, reviewer)
        return data
    
    def get_comments_count(self, obj):
        return obj.comments.count()


"""
The `TaskDetailSerializer` class provides `BoardTask` objects with fields for task details and related users such as assignee and reviewer.
"""
class TaskDetailSerializer(serializers.ModelSerializer):
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='reviewer', write_only=True, required=False, allow_null=True)
    assignee = UserNestedSerializer(read_only=True)
    reviewer = UserNestedSerializer(read_only=True)

    class Meta:
        model = BoardTask
        fields = ['id', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date', 'assignee', 'reviewer']
        read_only_fields = ['creator', 'board']


# The `BoardListSerializer` class provides a list of Board objects with additional fields for member count,ticket count, tasks to do count, and high priority tasks count.
class BoardListSerializer(serializers.ModelSerializer):
    members = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    class Meta: 
        model= Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id', 'members']
    """
    These functions calculate the count of the members, all tickets of the board, all tasks with the status `to do` or task with high priority
    """
    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        to_do_tasks = obj.tasks.filter(Q(status='to-do'))
        return to_do_tasks.count()

    def get_tasks_high_prio_count(self, obj):
        high_prio_tasks = obj.tasks.filter(Q(priority='high'))
        return high_prio_tasks.count()


"""
The `BoardDetailSerializer` class provides board details including specific details about members and tasks.
"""
class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserNestedSerializer(many=True, read_only=True)
    tasks = TaskListSerializer(many=True, read_only=True)
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'tasks']


"""
The `BoardDetailUpdateSerializer` class is only to provide a specific response for PATCH-requests. The responses are different to the `BoardDetailSerializer`
"""
class BoardDetailUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), write_only=True, required=False)
    owner_data = UserNestedSerializer(source="owner", read_only=True)
    members_data = UserNestedSerializer(source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members", "members_data"]

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        instance = super().update(instance, validated_data)
        if members is not None:
            instance.members.set(members)
        return instance
