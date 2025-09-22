from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status

"""
    The function `get_user_by_email` retrieves a user object based on the provided email address.
    :param email: it takes an email as a parameter and attempts to retrieve a User object from the database based on the provided email address. If the user with the given email is found, it returns the User object. If the user does not exist, it returns a 404 error or a 500 error.
    """
def get_user_by_email(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Internal Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)