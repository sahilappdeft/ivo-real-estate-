import ast
from jose import jwt
from django.conf import settings

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser


JWT_SECRET_KEY = settings.JWT_SECRET_KEY

class IsTokenValid(BasePermission):
    """
    Custom permission class to check if the token is valid and corresponds to a user.
    """

    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Token credentials not provided")# Token not in Bearer format, deny access
        
        token = auth_header.split(' ')[1]  # Extract token value from Bearer token

        if not token:
            # No token provided, deny access with appropriate message
            raise AuthenticationFailed("Token credentials not provided")
        
        try:
            # Decode the JWT token and extract the payload
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            user_data = payload.get("sub") 
            user_id =  ast.literal_eval(user_data).get('id')# Convert string to dictionary

            # Check if user ID exists
            if user_id is None:
                raise AuthenticationFailed("Invalid token")

            # Check if user with the given ID exists
            user = CustomUser.objects.filter(user_id=user_id).first()

            if user is None:
                raise AuthenticationFailed("Invalid token")

            # Add user object to the request
            request.user = user

            return True  # Return True if user exists, False otherwise
        except jwt.ExpiredSignatureError:
            # Token expired, deny access with appropriate message
            raise AuthenticationFailed("Token expired")
        except jwt.JWTError:
            # Error decoding token, deny access with appropriate message
            raise AuthenticationFailed("Unauthorized")
        
        
        
import ast
from jose import jwt
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser

JWT_SECRET_KEY = settings.JWT_SECRET_KEY

def token_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return redirect('login')
        
        token = auth_header.split(' ')[1]  # Extract token value from Bearer token

        if not token:
            return redirect('login')
        
        try:
            # Decode the JWT token and extract the payload
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            user_data = payload.get("sub")
            user_id = ast.literal_eval(user_data).get('id')  # Convert string to dictionary

            # Check if user ID exists
            if user_id is None:
                return redirect('login')

            # Check if user with the given ID exists
            user = CustomUser.objects.filter(user_id=user_id).first()

            if user is None:
                return redirect('login')

            # Add user object to the request
            request.user = user
            return view_func(request, *args, **kwargs)
        
        except jwt.ExpiredSignatureError:
            return redirect('login')
        except jwt.JWTError:
            return redirect('login')

    return _wrapped_view_func
