import jwt
from django.conf import settings
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from bitbucket_github.models import User


class JWTAuthentication:
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0] != b'Bearer':
            return None

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid Token. Token should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        return self.decode_token(token)

    def decode_token(self, payload):
        decoded_data = jwt.decode(payload, settings.SECRET_KEY, algorithms=['HS256'])

        username = decoded_data.get('username', None)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        return (user, payload)

    def authenticate_header(self, request):
        return 'Bearer'
