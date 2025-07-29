from django.shortcuts import render
from django.http import JsonResponse
from difflib import SequenceMatcher
import re
import unicodedata
from difflib import SequenceMatcher

def index(request):
    return render(request, 'fundanet/index.html')

def terceros(request):
    return render(request, 'fundanet/terceros.html')

def terceros_inicio(request):
    return render(request, 'fundanet/terceros_inicio.html')

def proyectos(request):
    return render(request, 'fundanet/proyectos.html')

def investigadores(request):
    return render(request, 'fundanet/investigadores.html')

def grupos(request):
    return render(request, 'fundanet/grupos.html')

def nodos(request):
    return render(request, 'fundanet/nodos.html')


def normalizar(nombre):
    nombre = nombre.lower()
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = nombre.encode('ascii', 'ignore').decode("utf-8")
    nombre = re.sub(r'\b(s\.a\.?|s\.l\.?|inc\.?|ltd\.?)\b', '', nombre)
    nombre = re.sub(r'[^a-z0-9]', '', nombre)
    return nombre.strip()

def buscar_terceros_duplicados(request):
    # ⚠️ Simulación temporal - reemplazar por llamada a API real en producción
    TERCEROS = [
        {"id": 1, "nombre": "Biogen"},
        {"id": 2, "nombre": "Biogen España, S.A."},
        {"id": 3, "nombre": "PharmaCorp"},
        {"id": 4, "nombre": "Pharma Corp."},
        {"id": 5, "nombre": "Pharma-Corp"},
    ]

    duplicados = []
    vistos = set()

    for i, t1 in enumerate(TERCEROS):
        nombre1 = normalizar(t1['nombre'])
        for j, t2 in enumerate(TERCEROS):
            if i >= j:
                continue
            nombre2 = normalizar(t2['nombre'])
            ratio = SequenceMatcher(None, nombre1, nombre2).ratio()
            if ratio >= 0.6:  # 👈 umbral más tolerante
                clave = tuple(sorted((t1['id'], t2['id'])))
                if clave not in vistos:
                    duplicados.append((t1, t2, round(ratio, 2)))
                    vistos.add(clave)

    return render(request, 'fundanet/terceros_duplicados.html', {
        'duplicados': duplicados
    })

