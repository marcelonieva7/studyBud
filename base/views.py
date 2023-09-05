from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import  login_required

from .models import Room, Topic
from .forms import RoomForm

def loginPage(req: HttpRequest):
  page = 'login'
  if req.user.is_authenticated:
    return redirect('base:home')

  if req.method == 'POST':
    username = req.POST.get('username').lower()
    password = req.POST.get('password')
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(req, 'el Usuario no existe')
    user = auth.authenticate(req, username=username, password=password)
    if user is not None:
      auth.login(req, user)
      return redirect('base:home')
    else: 
      messages.error(req, 'Usuario o contraseña invalida')
  context = {
    'page': page
  }
  return render(req, 'base/login_register.html', context)

def logoutUser(req):
  auth.logout(req)
  return redirect('base:home')

def registerPage(req: HttpRequest):
  form = UserCreationForm()
  if req.method == 'POST':
    form = UserCreationForm(req.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      auth.login(req, user)
      return redirect('base:login')
    else:
      messages.error(req, 'Ocurrio un error durante la registracion')

  context = {'form': form}  
  return render(req, 'base/login_register.html', context)

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

@login_required(login_url='/login')
def createRoom(req):
  form = RoomForm()

  if req.method == 'POST':
    form = RoomForm(req.POST)
    if form.is_valid():
      form.save()
      return redirect('base:home')
  context = {'form': form}
  return render(req, 'base/room_form.html', context)

@login_required(login_url='base:login')
def updateRoom(req: HttpRequest, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)

  if req.user != room.host:
    messages.error(req, 'Accion no permitida')
    return redirect('base:home')

  if req.method == 'POST':
    form = RoomForm(req.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('base:home')
  
  context = {'form': form}
  return render(req, 'base/room_form.html', context)

@login_required(login_url='base:login')
def deleteRoom(req, pk): 
  room = Room.objects.get(id=pk)

  if req.user != room.host:
    messages.error(req, 'Accion no permitida')
    return redirect('base:home')

  if req.method == 'POST':
    room.delete()
    return redirect('base:home')
  
  return render(req, 'base/delete.html', {'obj': room})
