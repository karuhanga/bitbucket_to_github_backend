import jwt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from bitbucket_github.models import User, Progress
from bitbucket_github.serializers import LoginSerializer, AuthorizeGithubSerializer, ProgressSerializer
from bitbucket_github.tasks import copy_to_github


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


@api_view(('POST',))
@login_required
def copy(request, repo_slug):
    user = request.user
    progress, created = Progress.objects.get_or_create(user=user, repo_slug=repo_slug)

    if not(progress.queued or progress.running):
        progress.queued = True
        progress.save()

        copy_to_github.delay(user.username, repo_slug)

    return Response({
        'message': f"Queued {repo_slug} for copying",
    })


@api_view(('GET',))
@login_required
def in_progress(request):
    user = request.user
    progress_items = Progress.objects.filter(user=user)
    serializer = ProgressSerializer(progress_items, many=True)

    return Response({
        'items': serializer.data,
    })
