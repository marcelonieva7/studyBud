from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Count, Q

from .models import Room, Topic
from .forms import RoomForm

def home(req):
  q = req.GET.get('q') if req.GET.get('q') != None else ''
  rooms = Room.objects.all().filter(
    Q(topic__name__icontains=q) | 
    Q(name__icontains=q) |
    Q(host__username__icontains=q) |
    Q(description__icontains=q)
    )
  topics = Topic.objects.all().annotate(top_topics=Count('room')).order_by('-top_topics')
  room_count = rooms.count()

  context = {
    'topics': topics,
    'rooms': rooms,
    'room_count': room_count
  }
  return render(req, 'base/home.html', context)

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

def deleteRoom(req, pk): 
  room = Room.objects.get(id=pk)

  if req.method == 'POST':
    room.delete()
    return redirect('base:home')
  
  return render(req, 'base/delete.html', {'obj': room})
