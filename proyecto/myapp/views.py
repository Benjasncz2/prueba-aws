from django.shortcuts import render
from django.http import HttpResponse 
from .models import *
from django.db import connection

def disponibilidad_boxes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                p.idPasillo,
                p.nombrePasillo,
                b.idBox,
                b.numeroBox,
                eb.descripcionEstadoBox
            FROM pasillo p
            JOIN box b ON b.idPasillo = p.idPasillo
            JOIN estadobox eb ON eb.idEstadoBox = b.idEstadoBox
            ORDER BY p.idPasillo, b.numeroBox;
        """)
        rows = cursor.fetchall()

    # Transformar a estructura útil para el template
    resultado = {}
    for row in rows:
        id_pasillo, nombre_pasillo, id_box, numero_box, estado_box = row
        if id_pasillo not in resultado:
            resultado[id_pasillo] = {
                'nombre': nombre_pasillo,
                'boxes': []
            }
        resultado[id_pasillo]['boxes'].append({
            'id': id_box,
            'numero': numero_box,
            'estado': estado_box
        })

    return render(request, 'home.html', {'pasillos': resultado})





def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')