from django.db import models
from django.contrib.auth.models import User

# The `STATUS_CHOICES` defines the possible choices for the `status` field in the `BoardTask` model. 
STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]


# The `PRIORITY_CHOICES` defines the possible choices for the `priority` field in the `BoardTask` model. 
PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]


# The `Board` class represents a model with a title, owner, members, and creation timestamp.
class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)


# The `BoardTask` class defines a model with fields for managing tasks associated with a board, including title, description, status, priority, due date, assignee, reviewer, creator, and creation timestamps.
class BoardTask(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="review_tasks")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_tasks")
    created_at = models.DateTimeField(auto_now_add=True)


# This class represents a TaskComment model with fields for task, author, content, and created_at timestamp.
class TaskComment(models.Model):
    task = models.ForeignKey(BoardTask, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_comments')
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
