from django.urls import path

from . import views

urlpatterns = [
    path('create_user', views.create_user , name = 'create_user'),
    path('login', views.login, name='login'),
]