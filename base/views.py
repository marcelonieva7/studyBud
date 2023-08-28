from django.shortcuts import render
from django.http import HttpResponse

def home(req):
  return HttpResponse("HOME VIEW")

def room(req):
  return HttpResponse("ROOM VIEW")
