import jwt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from bitbucket_github.models import User
from bitbucket_github.serializers import LoginSerializer, AuthorizeGithubSerializer


@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        existing_user = User.objects.get(username=serializer.validated_data['username'])
        serializer = LoginSerializer(existing_user, data=request.data)
        serializer.is_valid(raise_exception=True)
    except User.DoesNotExist:
        pass
    finally:
        user = serializer.save()

    token = jwt.encode({'username': user.username}, settings.SECRET_KEY, algorithm='HS256')
    return Response({
        'token': token,
        'username': user.username,
        'githubAuthenticated': user.github_authenticated()
    })


@api_view(('POST',))
@login_required
def authorize_github(request):
    serializer = AuthorizeGithubSerializer(request.user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({
        'message': "Successfully authorized github",
    })


@api_view(('POST',))
@login_required
def logout(request):
    user = request.user
    user.bitbucket_token = None
    user.github_token = None
    user.save()

    return Response({
        'message': "Successfully logged out.",
    })
