# from django.contrib import admin
from django.urls import path

from bitbucket_github.views import login, logout, authorize_github

urlpatterns = [
       path('login/', login),
       path('logout/', logout),
       path('authorize-github/', authorize_github),
]
