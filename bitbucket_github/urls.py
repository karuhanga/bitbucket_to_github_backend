# from django.contrib import admin
from django.urls import path

from bitbucket_github.views import login, logout, authorize_github, copy, in_progress

urlpatterns = [
       path('login/', login, name="login"),
       path('logout/', logout, name="logout"),
       path('authorize-github/', authorize_github, name="authorize_github"),
       path('copy/<str:repo_slug>/', copy, name="copy"),
       path('in-progress/', in_progress, name="in_progress"),
]
