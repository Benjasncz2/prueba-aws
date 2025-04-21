from django.shortcuts import render
from django.http import HttpResponse 
from .models import Pasillo, Box
from django.db import connection


def disponibilidad_boxes(request):
    pasillos = Pasillo.objects.prefetch_related(
        'box_set__idestadobox'
    ).all()

    return render(request, 'home.html', {'pasillos': pasillos})

def disponibilidad(request):
    pasillos = Pasillo.objects.prefetch_related('box_set__idestadobox').all()
    return render(request, 'home.html', {'pasillos': pasillos})


def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')