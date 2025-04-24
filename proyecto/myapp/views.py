from django.shortcuts import render
from django.http import HttpResponse 
from .models import Pasillo, Box
from django.db import connection
from django.db.models import Count, Q

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


def contador_boxes(request):
    pasillos = Pasillo.objects.prefetch_related('box_set').all()

    total_disponibles = 0
    pasillos_data = []

    for pasillo in pasillos:
        boxes = pasillo.box_set.all()
        disponibles = boxes.filter(idestadobox__descripcionestadobox="Disponible").count()
        total_disponibles += disponibles
        pasillos_data.append({
            'nombrepasillo': pasillo.nombrepasillo,
            'boxes': boxes,
            'disponibles': disponibles,  # Este campo es necesario para mostrar los disponibles
        })

    # Pasa los datos al template
    return render(request, 'home.html', {
        'pasillos': pasillos_data,
        'total_disponibles': total_disponibles,
    })
