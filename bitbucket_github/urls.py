# from django.contrib import admin
from django.urls import path

from bitbucket_github.views import login, authorize_github

urlpatterns = [
       path('login/', login),
       path('authorize-github/', authorize_github),
]
