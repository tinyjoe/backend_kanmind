from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response


"""
    The function `validate_board_member` checks if a user is a member of a board.
    :param board: provides the board object in which the user should be a member.
    :param user: the user who should be member of the board
    when the user does not exist in the provided board as a member a Validation Error is raised
    """
def validate_board_member(board, user):
    if not board.members.filter(id=user.id).exists():
        raise serializers.ValidationError({'error': 'User is not a member of the board'})


"""
    The function `validate_user in board` checks if a specific user is a member of a board.
    :param board: provides the board object in which the user should be a member.
    :param user_id: the id of the user who should be member of the board
    :param field_name: the string which should be shown in the error message (f.e. the full name of the user)
    when the user does not exist in the provided board as a member a Validation Error is raised
    """
def validate_user_in_board(board, user_id, field_name):
    if user_id is None:
        return
    if not board.members.filter(id=user_id).exists():
        raise serializers.ValidationError({'error': f'{field_name} has to be a member of the board.'})


"""
    The function `validate_email_address` checks if an email address is provided and validates its
    format.
    :param email: provided email address
    :return: The function `validate_email_address` is returning a Response object with an error message
    and status code if the email address is missing or has an invalid format. If the email address is
    valid, it returns None.
    """ 
def validate_email_address(email):
    if not email:
        return Response({'error': 'Email Address is missing.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_email(email)
    except ValidationError:
        return Response({'error': 'Invalid Email Format.'}, status=status.HTTP_400_BAD_REQUEST)
    return None
