from django.urls import path
from .views import BoardsView, TaskListView, BoardDetailView, TaskReviewingListView, AssignedTaskListView, CheckEmailView, TaskDetailView, TaskCommentListView, TaskCommentDeleteView

urlpatterns = [
    path('boards/', BoardsView.as_view(), name='boards_list'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/assigned-to-me/', AssignedTaskListView.as_view(), name='my_assigned_tasks'),
    path('tasks/reviewing/', TaskReviewingListView.as_view(), name='reviewing_tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:task_id>/comments/', TaskCommentListView.as_view(), name='task_comment_list'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', TaskCommentDeleteView.as_view(), name='task_comment_delete'),
    path('email-check/', CheckEmailView.as_view(), name='email-check'),
]