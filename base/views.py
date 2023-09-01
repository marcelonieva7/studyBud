from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Room
from .forms import RoomForm

def home(req):
  rooms = Room.objects.all()
  return render(req, 'base/home.html', {"rooms": rooms})

def room(req, pk):
  room = Room.objects.get(id=pk)
  return render(req, 'base/room.html', context={'room': room})

def createRoom(req):
  form = RoomForm()

  if req.method == 'POST':
    form = RoomForm(req.POST)
    if form.is_valid():
      form.save()
      return redirect('base:home')
  context = {'form': form}
  return render(req, 'base/room_form.html', context)

def updateRoom(req, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)

  if req.method == 'POST':
    form = RoomForm(req.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('base:home')
  
  context = {'form': form}
  return render(req, 'base/room_form.html', context)