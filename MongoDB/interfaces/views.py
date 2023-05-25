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
                return redirect('iniciar_sesion')
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

