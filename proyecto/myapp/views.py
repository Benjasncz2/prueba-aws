from django.shortcuts import render
from django.http import HttpResponse 
from .models import Pasillo, Box, Estadobox, Medico, Especialidad, Boximplemento, Implemento, Consulta, Paciente
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

def personal(request):
    busqueda = request.GET.get('busqueda', '')
    especialidad_id = request.GET.get('especialidad', '')
    
    medicos = Medico.objects.select_related('idespecialidad').all().order_by('apellidomedico')
    
    if busqueda:
        medicos = medicos.filter(
            Q(nombremedico__icontains=busqueda) | 
            Q(apellidomedico__icontains=busqueda)
        )
    
    if especialidad_id:
        medicos = medicos.filter(idespecialidad__idespecialidad=especialidad_id)
        especialidad_nombre = Especialidad.objects.get(
            idespecialidad=especialidad_id
        ).nombreespecialidad
    else:
        especialidad_nombre = None
    
    especialidades = Especialidad.objects.filter(
        idespecialidad__in=Medico.objects.values('idespecialidad').distinct()
    ).order_by('nombreespecialidad')
    
    return render(request, 'personal.html', {
        'medicos': medicos,
        'especialidades': especialidades,
        'busqueda_actual': busqueda,
        'especialidad_actual': especialidad_id,
        'especialidad_nombre': especialidad_nombre
    })

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

def box_detail(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    especialidad = box.especialidadbox
    estado = box.idestadobox.descripcionestadobox
    
    implementos = Implemento.objects.filter(
        boximplemento__idbox=box.idbox
    )

    consultas = Consulta.objects.filter(idbox=box.idbox).select_related('rutmedico', 'rutpaciente')

    turnos = []
    for consulta in consultas:
        try:
            medico = Medico.objects.get(rutmedico=consulta.rutmedico)
            medico_nombre = f'{medico.nombremedico} {medico.apellidomedico}'
        except Medico.DoesNotExist:
            medico_nombre = 'Sin médico asignado'
        
        try:
            paciente = Paciente.objects.get(rutpaciente=consulta.rutpaciente)
            paciente_nombre = f'{paciente.nombrepaciente} {paciente.apellidopaciente}'
        except Paciente.DoesNotExist:
            paciente_nombre = 'Sin paciente asignado'

        turnos.append({
            'medico': medico_nombre,
            'paciente': paciente_nombre,
            'fecha': consulta.fechaconsulta,
            'hora': consulta.horainicio
        })

    context = {
        'n_box': box.numerobox,
        'especialidad': especialidad,
        'estado': estado,
        'implementos': implementos,
        'turnos': turnos,
    }
    return render(request, 'box.html', context)

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

def dashboard(request):
    return render(request, 'dashboard.html')

def box(request):
    return render(request, 'box.html')