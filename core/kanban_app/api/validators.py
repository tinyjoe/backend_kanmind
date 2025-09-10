from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

def validate_board_member(board, user):
    if not board.members.filter(id=user.id).exists():
        raise serializers.ValidationError({'error': 'User is not a member of the board'})
    
def validate_user_in_board(board, user_id, field_name):
    if user_id is None:
        return
    if not board.members.filter(id=user_id).exists():
        raise serializers.ValidationError({'error': f'{field_name} has to be a member of the board.'})
    
def validate_email_address(email):
        if not email:
            return Response({'error': 'Email Address is missing.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid Email Format.'}, status=status.HTTP_400_BAD_REQUEST)
        return None