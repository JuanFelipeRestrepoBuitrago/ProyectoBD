from django.shortcuts import render, redirect
from .models import Estudiantes, Clases, Materias, Profesores
from django.http import HttpResponse
from .forms import EstudianteForm
from datetime import datetime
from django.db import transaction
from django.contrib import messages


def registro_estudiante(request):
    return render(request, 'Principales/registro_estudiante.html')


def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        try:
            estudiante = Estudiantes.objects.get(documento_identidad=usuario)
            if estudiante.contraseña == contraseña:
                return redirect('principal_estudiante', documento=usuario)
            else:
                messages.error(request, "Error verificacion")
                return redirect('iniciar_sesion')
        except (Estudiantes.DoesNotExist, ValueError):
            messages.info(request, "No existe usuario")
            return redirect('iniciar_sesion')
    else:
        return render(request, 'Principales/iniciar_sesion.html', {
                      'title': 'Iniciar Sesión',
                      })


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
            'title': 'Home',
        })
    else:
        estudiante.nombre_completo = request.POST['nombre_completo']
        estudiante.documento_identidad = request.POST['documento']
        estudiante.programa_academico = request.POST['programa_academico']
        estudiante.save()
        return redirect('principal_estudiante', documento=estudiante.documento_identidad)


def cambiar_constraseña(request):
    pass


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
        return redirect('clases estudiante', documento=estudiante.documento_identidad)