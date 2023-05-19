from django.shortcuts import render, redirect
from .models import Estudiantes, Clases, Materias, Profesores
from django.http import HttpResponse
from .forms import EstudianteForm
from datetime import datetime
from django.db import transaction
from django.contrib import messages


def interfaz_eleccion(request):
    return render(request, 'Interfaces/archivo.html')


def registro_estudiante(request):
    return render(request, 'Interfaces/registro_estudiante.html')


def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        try:
            estudiante = Estudiantes.objects.get(documento_identidad=usuario)
            if estudiante.contraseña == contraseña:
                return redirect('home_estudiante', documento=usuario)
            else:
                messages.error(request, "Error verificacion")
                return redirect('interfaz_eleccion')
        except (Estudiantes.DoesNotExist, ValueError):
            messages.info(request, "No existe usuario")
            return redirect('interfaz_eleccion')


@transaction.atomic
def registrar_estudiante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        documento = request.POST.get('documento')
        programa = request.POST.get('programa_academico')
        contraseña = request.POST.get('contraseña')
        contraseña_c = request.POST.get('contraseña_c')

        if contraseña_c != contraseña:
            messages.error(request,'Las contraseñas no son iguales')
            return redirect('registro_estudiante')


@transaction.atomic
def home_estudiante(request, documento):
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    if request.method == 'GET':
        return render(request, 'Estudiante/estudiante.html', {
            'estudiante': estudiante,
            'form': EstudianteForm()
        })
    else:
        if request.POST['nombre_completo'] != '':
            estudiante.nombre_completo = request.POST['nombre_completo']
        if request.POST['documento_identidad'] != '':
            estudiante.documento_identidad = request.POST['documento_identidad']
        if request.POST['programa_academico'] != '':
            estudiante.programa_academico = request.POST['programa_academico']
        if request.POST['contraseña'] != '':
            estudiante.contraseña = request.POST['contraseña']
        estudiante.save()
        return redirect('home_estudiante', documento=estudiante.documento_identidad)


@transaction.atomic
def get_clases(request, documento):
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    registros = estudiante.registro_set.filter(fecha_registro__year=datetime.now().year)
    clases = Clases.objects.filter(id_clase__in=registros.values('id_clase'))
    materias = Materias.objects.filter(id_materia__in=clases.values('id_materia'))
    profesores = Profesores.objects.filter(id_profesor__in=clases.values('id_profesor'))
    if request.method == 'GET':
        return render(request, 'Estudiante/clases.html', {
            'estudiante': estudiante,
            'clases': clases,
            'materias': materias,
            'profesores': profesores
        })
    else:
        clase = request.POST['clase']
        clase = int(str(clase).split('-')[1])
        registro = registros.filter(id_clase=clase, fecha_registro__year=datetime.now().year)

        registro.delete()
        return redirect('get_clases', documento=estudiante.documento_identidad)