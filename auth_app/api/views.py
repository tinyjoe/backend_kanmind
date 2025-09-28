from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .services import authenticate_user_by_email


# The `UserRegistrationView` class handles user registration requests by validating user input,
# creating a new user instance, generating an authentication token, and returning relevant user data
# or error messages.
class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            saved_user = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_user)
            data = {'token': token.key, 'fullname': saved_user.username, 'email': saved_user.email, 'user_id': saved_user.id}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# The `UserLoginView` class handles user authentication by validating login credentials and gets the generated
# a token for the authenticated user.
class UserLoginView(ObtainAuthToken): 
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate_user_by_email(email, password)
        if user is None:
            return Response({'error': 'Invalid email address or password.'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        data = {'token': token.key, 'fullname': user.username, 'email': user.email, 'user_id': user.id}
        return Response(data, status=status.HTTP_200_OK)
        