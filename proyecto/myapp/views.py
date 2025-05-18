from django.shortcuts import render
from django.http import HttpResponse 
from .models import Pasillo, Box, Estadobox, Medico, Especialidad, Boximplemento, Consulta, Paciente, Implemento
from django.db import connection
from django.db.models import Count, Q, Value, CharField
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta, time, datetime

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

def agenda(request):
    ahora_local = timezone.localtime(timezone.now())
    fecha_hoy = ahora_local.date()
    hora_actual = ahora_local.time()
    
    mostrar_actuales = 'mostrar_actuales' in request.GET
    
    # Obtener parámetros de filtro
    filtro_medico = request.GET.get('medico', '')
    filtro_paciente = request.GET.get('paciente', '')
    
    if mostrar_actuales:
        fecha_seleccionada = fecha_hoy
    else:
        try:
            fecha_seleccionada = date.fromisoformat(request.GET.get('fecha', fecha_hoy.isoformat()))
        except ValueError:
            fecha_seleccionada = fecha_hoy
    
    consultas = Consulta.objects.select_related(
        'rutmedico', 'rutpaciente', 'idbox'
    ).filter(
        fechaconsulta=fecha_seleccionada
    ).order_by('horainicio')
    
    # Aplicar filtros
    if filtro_medico:
        consultas = consultas.filter(
            Q(rutmedico__nombremedico__icontains=filtro_medico) |
            Q(rutmedico__apellidomedico__icontains=filtro_medico)
        )
    
    if filtro_paciente:
        consultas = consultas.filter(
            Q(rutpaciente__nombrepaciente__icontains=filtro_paciente) |
            Q(rutpaciente__apellidopaciente__icontains=filtro_paciente)
        )
    
    if mostrar_actuales:
        consultas = consultas.filter(horainicio__gte=hora_actual)
    
    return render(request, 'agenda.html', {
        'consultas': consultas,
        'fecha_seleccionada': fecha_seleccionada,
        'hoy': fecha_hoy,
        'hora_actual': hora_actual,
        'mostrar_actuales': mostrar_actuales
    })

def box_detail(request, box_id):
    box = get_object_or_404(Box, pk=box_id)
    especialidad = box.especialidadbox
    estado = box.idestadobox.descripcionestadobox
    implementos = Implemento.objects.filter(boximplemento__idbox=box.idbox).values_list('nombreimplemento', flat=True)

    fecha_filtro = request.GET.get('fecha', '')
    medico_filtro = request.GET.get('medico', '')
    paciente_filtro = request.GET.get('paciente', '')
    
    consultas = Consulta.objects.filter(idbox=box.idbox)

    if fecha_filtro:
        consultas = consultas.filter(fechaconsulta=fecha_filtro)
    if medico_filtro:
        # Normaliza espacios y busca por nombre completo en ambos órdenes
        medico_filtro_normalizado = ' '.join(medico_filtro.split())
        consultas = consultas.annotate(
            medico_completo=Concat(
                'rutmedico__nombremedico',
                Value(' '),
                'rutmedico__apellidomedico',
                output_field=CharField()
            ),
            medico_completo_inv=Concat(
                'rutmedico__apellidomedico',
                Value(' '),
                'rutmedico__nombremedico',
                output_field=CharField()
            )
        ).filter(
            Q(rutmedico__nombremedico__icontains=medico_filtro_normalizado) |
            Q(rutmedico__apellidomedico__icontains=medico_filtro_normalizado) |
            Q(medico_completo__icontains=medico_filtro_normalizado) |
            Q(medico_completo_inv__icontains=medico_filtro_normalizado)
        )
    if paciente_filtro:
        paciente_filtro_normalizado = ' '.join(paciente_filtro.split())
        consultas = consultas.annotate(
            paciente_completo=Concat(
                'rutpaciente__nombrepaciente',
                Value(' '),
                'rutpaciente__apellidopaciente',
                output_field=CharField()
            ),
            paciente_completo_inv=Concat(
                'rutpaciente__apellidopaciente',
                Value(' '),
                'rutpaciente__nombrepaciente',
                output_field=CharField()
            )
        ).filter(
            Q(rutpaciente__nombrepaciente__icontains=paciente_filtro_normalizado) |
            Q(rutpaciente__apellidopaciente__icontains=paciente_filtro_normalizado) |
            Q(paciente_completo__icontains=paciente_filtro_normalizado) |
            Q(paciente_completo_inv__icontains=paciente_filtro_normalizado)
        )

    consultas = consultas.order_by('fechaconsulta', 'horainicio').select_related('rutmedico', 'rutpaciente')

    turnos = []
    for consulta in consultas:

        try:
            medico = consulta.rutmedico
            medico_nombre = f'{medico.nombremedico} {medico.apellidomedico}'
        except Medico.DoesNotExist:
            medico_nombre = 'Sin médico asignado'

        try:
            paciente = consulta.rutpaciente
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


def dashboard(request):
    total_boxes = Box.objects.count()
    en_uso = Box.objects.filter(idestadobox=2).count()
    disponibles = Box.objects.filter(idestadobox=1).count()
    en_mantencion = Box.objects.filter(idestadobox=3).count()

    porcentajes = {
        'en_uso': round((en_uso / total_boxes * 100), 1) if total_boxes > 0 else 0,
        'disponibles': round((disponibles / total_boxes * 100), 1) if total_boxes > 0 else 0,
        'en_mantencion': round((en_mantencion / total_boxes * 100), 1) if total_boxes > 0 else 0,
    }

    
    horas = ['08:00','08:30','09:00','09:30','10:00','10:30','11:00','11:30','12:00', '12:30', '13:00', '13:30', '14:00','14:30','15:00','15:30', '16:00', '16:30', '17:00']
    disponibilidad_por_hora = []
    hoy = date.today()

    for hora_str in horas:
       
        hora = datetime.strptime(hora_str, '%H:%M').time()
        
       
        boxes_en_uso = Consulta.objects.filter(
            fechaconsulta=hoy,
            horainicio__lte=hora,
            horafin__gte=hora
        ).count()
        
        disponibles_hora = total_boxes - boxes_en_uso - en_mantencion
        disponibilidad_por_hora.append(max(disponibles_hora, 0))

    context = {
        'total_boxes': total_boxes,
        'en_uso': en_uso,
        'disponibles': disponibles,
        'en_mantencion': en_mantencion,
        'porcentajes': porcentajes,
        'horas': horas,
        'disponibilidad_por_hora': disponibilidad_por_hora,
    }
    return render(request, 'dashboard.html', context)

def box(request):
    return render(request, 'box.html')