from django.shortcuts import render
from django.http import HttpResponse 
from .models import Pasillo, Box, Estadobox, Medico, Boximplemento
from django.db import connection
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def disponibilidad_boxes(request):
    pasillos = Pasillo.objects.prefetch_related(
        'box_set__idestadobox'
    ).all()

    total_disponibles = 0
    pasillos_data = []

    for pasillo in pasillos:
        boxes = pasillo.box_set.all()
        disponibles = sum(1 for box in boxes if box.idestadobox.descripcionestadobox == "Disponible")
        total_disponibles += disponibles

        pasillos_data.append({
            'pasillo': pasillo,
            'boxes': boxes,
            'disponibles': disponibles
        })

    return render(request, 'boxes.html', {
        'pasillos_data': pasillos_data,
        'total_disponibles': total_disponibles
    })


def disponibilidad(request):
    pasillos = Pasillo.objects.prefetch_related('box_set__idestadobox').all()
    return render(request, 'boxes.html', {'pasillos': pasillos})


def cambiar_estado_implemento(request, implemento_id, box_id, nuevo_estado):
    try:
        box_implemento = get_object_or_404(
            Boximplemento,
            idimplemento=implemento_id,
            idbox=box_id
        )
        
        if box_implemento.cambiar_estado(nuevo_estado):
            messages.success(request, "Estado del implemento actualizado")
        else:
            messages.error(request, "No se pudo cambiar el estado")
            
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    
    return redirect('Implementos.html')



def implementos(request):
    return render(request, 'Implementos.html')

def login(request):
    return render(request, 'login.html')

def boxes(request):
    return render(request, 'boxes.html')

def panel_admin(request):
    return render(request, 'panel_admin.html')

def agenda(request):
    return render(request, 'agenda.html')

def personal(request):
    medicos = Medico.objects.all().order_by('apellidomedico')
    return render(request, 'personal.html', {'medicos': medicos})

def dashboard(request):
    return render(request, 'dashboard.html')