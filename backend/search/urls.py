from django.urls import path, include
from django.contrib import admin
from . import api

urlpatterns = [
    path('', api.search, name='search')
]
