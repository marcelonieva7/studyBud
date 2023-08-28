from django.shortcuts import render
from django.http import HttpResponse

def home(req):
  return render(req, 'base/home.html')

def room(req):
  return render(req, 'base/room.html')
