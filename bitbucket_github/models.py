import requests
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bitbucket_token = models.CharField(max_length=200, null=True)
    github_token = models.CharField(max_length=200, null=True)

    def github_authenticated(self):
        if self.github_token is None:
            return False
        r = requests.get(url='https://api.github.com/user',
                         headers={'Authorization': f'token {self.github_token}'}
                         )
        if r.status_code == 200:
            return True
        return False
