from django.contrib.auth.models import User

from rest_framework import serializers

from .validators import validate_passwords, validate_unique_email
from .services import create_new_user


# This class defines a serializer for user registration with fields for fullname, email, password, and
# repeated password, along with validation and saving methods.
class UserRegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=255)
    repeated_password = serializers.CharField(write_only=True)
    class Meta: 
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {'password': {'write_only': True}}

    """
    The function saves a new user with validated data after checking password and email uniqueness.
    This function is creating a new user with the validated data (email, password, fullname) that was passed in after performing validations on the password and email.
    """
    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']
        fullname = self.validated_data['fullname']
        validate_passwords(pw, repeated_pw)
        validate_unique_email(email)
        return create_new_user(email=email, password=pw, fullname=fullname)
    

# The class `UserLoginSerializer` defines a serializer for user login data with fields for email and
# password.
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)