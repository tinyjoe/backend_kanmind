from django.contrib.auth.models import User
from rest_framework import serializers

def validate_passwords(password, repeated_password):
    if password != repeated_password:
        raise serializers.ValidationError({'error': 'Passwords dont match'})

def validate_unique_email(email):
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError({'error': 'Email already exists'})