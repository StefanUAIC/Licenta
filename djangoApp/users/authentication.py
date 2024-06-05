from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(token)
            user = jwt_authenticator.get_user(validated_token)
            request.user = user
            return user
        except InvalidToken:
            return None


jwt_auth = JWTAuth()
