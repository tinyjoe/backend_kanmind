from django.contrib.auth.models import User
from rest_framework import serializers

def validate_board_member(board, user):
    if not board.members.filter(id=user.id).exists():
        raise serializers.ValidationError({'error': 'User is not a member of the board'})
    
def validate_user_in_board(board, user_id, field_name):
    if user_id is None:
        return
    if not board.members.filter(id=user_id).exists():
        raise serializers.ValidationError({'error': f'{field_name} has to be a member of the board.'})