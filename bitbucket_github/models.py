from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bitbucket_token = models.CharField(max_length=200, null=True)
    github_token = models.CharField(max_length=200, null=True)
