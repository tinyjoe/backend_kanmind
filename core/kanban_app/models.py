from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)


class BoardTask(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    duedate = models.DateField(auto_now_add=True)
    assignee = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assigned_task')
    reviewer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reviewed_task')

class TaskComment(models.Model):
    task = models.ForeignKey(BoardTask, on_delete=models.CASCADE, related_name='comments')
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
