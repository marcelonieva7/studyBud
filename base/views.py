from django.shortcuts import render
from django.http import HttpResponse

ROOMS = [
  {
    "id": 1,
    "name": 'room 01',
  },
  {
    "id": 2,
    "name": 'room 02',
  },
  {
    "id": 3,
    "name": 'room 03',
  }
]

def home(req):
  return render(req, 'base/home.html', {"rooms": ROOMS})

def room(req, pk):
  context = {
    'room': None
  }
  for r in ROOMS:
    if pk == r["id"]:
      context["room"] = r

  return render(req, 'base/room.html', context=context)
