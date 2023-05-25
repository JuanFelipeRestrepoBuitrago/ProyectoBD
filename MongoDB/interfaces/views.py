from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
#from djongo import transaction // tal parece que no funciona
from django.db import IntegrityError
from collections import OrderedDict
import json

# Create your views here.

#Inicio Sesion
def login(request):
    if request.method == 'GET':
        return render(request, 'Principales/iniciar_sesion.html',{
            'title' : 'Iniciar Sesion'
        })
    else:
        nombre = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        try:
            estudiante = Estudiantes.objects.get(documento_identidad=nombre)
            if estudiante.contraseña == contraseña:
                messages.error(request, "Verificación correcta")
                return redirect('principal_estudiante',documento=nombre)
            else:
                messages.error(request, "Error verificacion")
                return redirect('iniciar_sesion')
        except (Estudiantes.DoesNotExist, ValueError):
            messages.info(request, "No existe usuario")
            return redirect('iniciar_sesion')

#Registro Estudiante
def registro_estudiante(request):
        if request.method == "GET":
            return render(request, 'Principales/registro_estudiante.html', {
                'title': 'Registrar Estudiante',
            })
        else:
            documento = request.POST.get('documento')
            nombre = request.POST.get('nombre')
            programa_academico = request.POST.get('programa_academico')
            contraseña = request.POST.get('contraseña')
            contraseña_c = request.POST.get('contraseña_c')
            try:
                if contraseña != contraseña_c:
                    messages.error(request, 'Las contraseñas no coinciden')
                    return redirect('registro_estudiante')

                horario = OrderedDict()
                horario['apro'] = []

                estudent = Estudiantes(documento_identidad=documento, nombre_completo=nombre,programa_academico=programa_academico, contraseña=contraseña, aprobadas=horario)
                estudent.save()

                messages.success(request, 'Usuario creado con éxito')
                return redirect('iniciar_sesion')
            except ValueError:
                messages.error(request, 'Error al crear usuario')
                return redirect('registro_estudiante')
            except IntegrityError:
                messages.error(request, 'El usuario con ese documento ya existe')
                return redirect('registro_estudiante')
            except:
                messages.error(request, 'Error de registro')
                return redirect('registro_estudiante')

#Cambiar contraseña
def cambiar_constraseña(request):
    if request.method == 'GET':
        return render(request, 'Principales/contraseña.html', {
            'title': 'Cambiar Contraseña',
        })
    else:
        documento = request.POST['documento']
        contraseña = request.POST['contraseña']
        contraseña_c = request.POST['contraseña_confirmación']

        try:
            estudiante = Estudiantes.objects.get(documento_identidad=documento)
            if contraseña != contraseña_c:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('cambiar_contraseña')
            else:
                estudiante.contraseña = contraseña
                estudiante.save()
                messages.success(request, 'Contraseña modificada con éxito')
                return redirect('iniciar_sesion')
        except Estudiantes.DoesNotExist:
            messages.info(request, 'Usuario no existente')
            return redirect('iniciar_sesion')


#Pagina de inicio para estudiante
def home_estudiante(request, documento):
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    if request.method == 'GET':
        return render(request, 'Estudiantes/estudiante.html', {
            'estudiante': estudiante,
            'title': 'Home',
        })
    else:
        estudiante.nombre_completo = request.POST['nombre_completo']
        estudiante.documento_identidad = request.POST['documento']
        estudiante.programa_academico = request.POST['programa_academico']
        estudiante.save()
        messages.success(request, 'Datos modificados con éxito')
        return redirect('principal_estudiante', documento=estudiante.documento_identidad)

#Ver las clases
def get_clases(request,documento):
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    registros = Registros.objects.filter(codigo_estudiante=estudiante.id, fecha_registro__year=datetime.now().year)
    clases = Clases.objects.filter(id__in=registros.values('id'))
    if request.method == 'GET':
        return render(request, 'Estudiantes/clases.html', {
            'title': f'Clases {estudiante.nombre_completo}',
            'estudiante': estudiante,
            'clases': clases,
        })
    else:
        clase = request.POST['id_clase']
        registro = Registros.get(id_clase=clase)

        registro.delete()
        messages.success(request, 'Materia eliminada con éxito')
        return redirect('clases_estudiante', documento=estudiante.documento_identidad)
