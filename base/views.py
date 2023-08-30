from django.shortcuts import render
from django.http import HttpResponse

from .models import Room

def home(req):
  rooms = Room.objects.all()
  return render(req, 'base/home.html', {"rooms": rooms})

def room(req, pk):
  room = Room.objects.get(id=pk)
  return render(req, 'base/room.html', context={'room': room})
