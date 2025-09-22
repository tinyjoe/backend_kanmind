from django.contrib.auth.models import User

from rest_framework import serializers


"""
    The function `validate_passwords` checks if two passwords match and raises an error if they don't.
    :param password: The `password` parameter is a string that represents a user's chosen
    password.
    :param repeated_password: The `repeated_password` parameter is used to confirm the password entered by the user. 
    The function `validate_passwords` compares the `password` and `repeated_password
    """
def validate_passwords(password, repeated_password):
    if password != repeated_password:
        raise serializers.ValidationError({'error': 'Passwords dont match'})


"""
    The function `validate_unique_email` checks if a given email already exists in the database and
    raises a validation error if it does.
    :param email: The `email` parameter is the email address of the created user
    If the email is found in the `User` model, it raises a `serializers.ValidationError`.
    """
def validate_unique_email(email):
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError({'error': 'Email already exists'})