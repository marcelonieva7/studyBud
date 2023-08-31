from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
  path('', views.home, name='home'),
  path('room/<int:pk>', views.room, name='room'),
  path('create-room', views.createRoom, name='create-room'),
]