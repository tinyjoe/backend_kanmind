from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status


def get_user_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Internal Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)