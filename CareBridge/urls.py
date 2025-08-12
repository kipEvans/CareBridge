
from django.contrib import admin
from django.urls import path,include
from hospitalapp import views

urlpatterns = [
    path('', include('hospitalapp.urls')),
]
