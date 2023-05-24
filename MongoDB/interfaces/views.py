from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

# Create your views here.

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

