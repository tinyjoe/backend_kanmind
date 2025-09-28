from django.contrib.auth import authenticate
from django.contrib.auth.models import User

"""
    The function creates a new user with the provided email, password, and full name.
    It takes three parameters: `email`, `password`, and `fullname` and creates a new user object with the provided email and full name, sets the password for the user, saves the user object, and then returns the newly created user object
    :param email: should be the email address of the newly created user
    :param password: the password of the newly created user
    :param fullname: the full name of the created user, gets saved into the default field username of the User Object
    :return: the user object that will be created gets returned
    """
def create_new_user(email, password, fullname):
    new_user = User(email=email, username=fullname)
    new_user.set_password(password)
    new_user.save()
    return new_user


    """
    The function `authenticate_user_by_email` attempts to authenticate a user by their email and
    password.
    :param email: The `email` parameter is a string that represents the email address of the user trying
    to authenticate
    :param password: The `password` parameter is a string that represents the password input provided by the user for authentication. This password will be used to authenticate the user along with their email address
    :return: the authenticated user object if the user with the provided email exists and the password
    is correct. If the user does not exist or the password is incorrect, it will return None.
    """
def authenticate_user_by_email(email: str, password: str):
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    user = authenticate(username=user_obj.username, password=password)
    return user