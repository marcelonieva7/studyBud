from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest
from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages, auth
from django.contrib.auth.decorators import  login_required

from .models import Room, Topic, Message
from .forms import RoomForm, CommentForm

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
  room_msg = Message.objects.all().filter(
    Q(room__topic__name__icontains=q)
  )

  context = {
    'topics': topics,
    'rooms': rooms,
    'room_count': room_count,
    'room_msg': room_msg
  }
  return render(req, 'base/home.html', context)

def room(req: HttpRequest, pk):
  room = Room.objects.get(id=pk)
  room_messages = room.message_set.all().order_by('-created')
  participants = room.participants.all()

  form = CommentForm(initial={'user': req.user, 'room': room})

  if req.method == 'POST':
    form = CommentForm(req.POST)
    if form.is_valid:
      msg = form.save()
      room.participants.add(req.user)
      return redirect(reverse('base:room', kwargs={'pk':pk}))
  context = {
    'form': form,
    'room': room,
    'room_messages': room_messages,
    'participants': participants
  }
  return render(req, 'base/room.html', context)

def userProfile(req: HttpRequest, pk):
  user = User.objects.get(pk=pk)
  context = {
    'user': user
  }
  return render(req, 'base/profile.html', context)

@login_required(login_url='/login')
def createRoom(req):
  form = RoomForm()

  if req.method == 'POST':
    form = RoomForm(req.POST)
    if form.is_valid():
      form.save()
      return redirect('base:home')
  context = {'form': form}
  return render(req, 'base/form.html', context)

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
  return render(req, 'base/form.html', context)

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

@login_required(login_url='base:login')
def deleteMsg(req, pk): 
  msg = Message.objects.get(id=pk)
  room_id = msg.room.pk

  if req.user != msg.user:
    messages.error(req, 'Accion no permitida')
    return redirect('base:room', pk=room_id)

  if req.method == 'POST':
    msg.delete()
    return redirect('base:room', pk=room_id)
  
  return render(req, 'base/delete.html', {'obj': msg})

@login_required(login_url='base:login')
def editMsg(req, pk): 
  msg = Message.objects.get(id=pk)
  room_id = msg.room.pk
  form = CommentForm(instance=msg)

  if req.user != msg.user:
    messages.error(req, 'Accion no permitida')
    return redirect('base:room', pk=room_id)

  if req.method == 'POST':
    form = CommentForm(req.POST, instance=msg)
    if form.is_valid:
      form.save()
      return redirect('base:room', pk=room_id)

  context = {
    'form': form
  }  
  return render(req, 'base/form.html', context)
