from tokenize import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')

        if raw_token is None:
            return None

        # validated_token = self.get_validated_token(raw_token)

        # return self.get_user(validated_token), validated_token
        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError):
            # 🔥 Ignore invalid token silently
            return None

        return self.get_user(validated_token), validated_token
