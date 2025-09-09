from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .services import authenticate_user_by_email

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            saved_user = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_user)
            data = {'token': token.key, 'fullname': saved_user.username, 'email': saved_user.email, 'user_id': saved_user.id}
        else:
            data=serializer.errors
        return Response(data)
    
class UserLoginView(ObtainAuthToken): 
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate_user_by_email(email, password)
        else:
            return Response({'error': 'Invalid login credentials'}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        data = {'token': token.key, 'fullname': user.username, 'email': user.email, 'user_id': user.id}
        return Response(data)