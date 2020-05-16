from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from api import views

urlpatterns = [
    url('^login/',views.LoginView.as_view()),
    url('^message/',views.GetMessageView.as_view()),
]
