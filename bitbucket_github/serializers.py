import requests
from django.conf import settings
from rest_framework import serializers

from bitbucket_github.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    bitbucket_token = serializers.CharField(max_length=200)

    def validate_bitbucket_token(self, value):
        r = requests.get(f'https://api.bitbucket.org/2.0/user?access_token=${value}')
        if r.status_code == 200:
            return value
        raise serializers.ValidationError("Bitbucket token is invalid")

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.bitbucket_token = validated_data['bitbucket_token']
        instance.save()
        return instance


class AuthorizeGithubSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=200)

    def create(self, validated_data):
        pass

    def validate_code(self, value):
        response = requests.post('https://github.com/login/oauth/access_token',
                                 data={'client_id': settings.GITHUB['CLIENT_ID'],
                                  'client_secret': settings.GITHUB['CLIENT_SECRET'],
                                  'code': value},
                                 headers={'Accept': 'application/json'})

        if response.status_code == 200:
            return response.json()['access_token']
        raise serializers.ValidationError("Github code is invalid")

    def update(self, instance, validated_data):
        instance.github_token = validated_data['code']
        instance.save()
        return instance
