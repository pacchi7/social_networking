import jwt
from django.conf import settings
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthenticationPermission(permissions.BasePermission):
    """
    Permission class to enforce JWT (JSON Web Token) authentication for a view.
    """
    def has_permission(self, request, view):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')

        if not authorization_header:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        try:
            token_prefix, token = authorization_header.split(' ')
            if token_prefix.lower() != 'bearer':
                raise AuthenticationFailed('Authorization header must start with Bearer')
            decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_payload.get('user_id')
            user_role = decoded_payload.get('role')
            if user_id is None:
                raise AuthenticationFailed('Invalid token. Missing required claims.')

            User = get_user_model()
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed('No such user exists.')

            request.user = user
            return True

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
        return False
