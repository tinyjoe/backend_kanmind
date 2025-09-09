from django.contrib import admin
from django.urls import path
from .views import BoardsView, TaskListView, BoardDetailView

urlpatterns = [
    path('boards/', BoardsView.as_view(), name='boards_list'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('tasks/', TaskListView.as_view(), name='task_list')
]