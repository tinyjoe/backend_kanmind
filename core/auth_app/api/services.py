from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def create_new_user(email, password, fullname):
    new_user = User(email=email, username=fullname)
    new_user.set_password(password)
    new_user.save()
    return new_user

def authenticate_user_by_email(email: str, password: str):
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    user = authenticate(username=user_obj.username, password=password)
    return user