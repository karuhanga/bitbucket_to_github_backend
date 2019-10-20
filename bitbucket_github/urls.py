# from django.contrib import admin
from django.urls import path

from bitbucket_github.views import login, logout, authorize_github, copy, in_progress

urlpatterns = [
       path('login/', login),
       path('logout/', logout),
       path('authorize-github/', authorize_github),
       path('copy/<str:repo_slug>/', copy),
       path('in-progress/', in_progress),
]
