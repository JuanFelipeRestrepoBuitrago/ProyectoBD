from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError, models
from mongoengine import *
from .pipelines import *

from datetime import datetime
from mongoengine.queryset.visitor import Q


def login(request):
    """
    Vista para iniciar sesión, los datos son recibidos por método POST, se verifica que el usuario exista
    primero como estudiante, si no existe se verifica como administrador, sino se muestra un mensaje de error
    y se redirige a la página de inicio de sesión.

    :param request: HttpRequest
    :return: HttpResponse, interfaz de inicio de sesión
    """
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

def registro_estudiante(request):
    """
    Vista para registrar un estudiante en la base de datos, los datos son recibidos por método POST,
    se verifica que las contraseñas coincidan y que el documento no exista en la base de datos,
    si todo sale bien se crea el usuario y se redirige a la página de inicio de sesión, sino se
    muestra un mensaje de error y se redirige a la página de registro de estudiante.

    :param request: HttpRequest
    :return: HttpResponse, interfaz de registro de estudiantes
    """
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
            siguiente_id = next_id('Estudiantes')
            estudent = Estudiantes(id_estudiante = siguiente_id, documento_identidad=documento, nombre_completo=nombre,
                                   programa_academico=programa_academico, contraseña=contraseña).save()

            messages.success(request, 'Usuario creado con éxito')
            return redirect('iniciar_sesion')
        except ValueError:
            messages.error(request, 'Error al crear usuario')
            return redirect('registro_estudiante')
        except IntegrityError:
            messages.error(request, 'El usuario con ese documento ya existe')
            return redirect('registro_estudiante')
'''        except:
            messages.error(request, 'Error de registro')
            return redirect('registro_estudiante')'''

def cambiar_constraseña(request):
    """
    Vista para cambiar la contraseña del estudiante, los datos son recibidos por método POST,
    se verifica que las contraseñas coincidan, sino se muestra un error en esta página,
    y que el documento exista en la base de datos, sino se redirige a la página de iniciar sesión
    con un mensaje de error. Finalmente, si todo está correcto,se redirige a la página de inicio de sesión.

    :param request: HttpRequest
    :return: HttpResponse, interfaz de cambio de contraseña del estudiante
    """
    if request.method == 'GET':
        return render(request, 'Principales/contraseña.html', {
            'title': 'Cambiar Contraseña',
        })
    else:
        documento = request.POST['documento']
        contraseña = request.POST['contraseña']
        contraseña_c = request.POST['contraseña_confirmación']

        try:
            #estudiante = Estudiantes.objects(documento_identidad=documento)
            query = buscar_estudiante_documento(documento)
            estudiantes = Estudiantes.objects.aggregate(query)
            if contraseña != contraseña_c:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('cambiar_contraseña')
            else:
                for estudiante in estudiantes:
                    estudiante_modificado = Estudiantes.objects.get(id=estudiante['_id'])
                    estudiante_modificado.update(contraseña=contraseña)
                #estudiante.update(contraseña=contraseña)
                messages.success(request, 'Contraseña modificada con éxito')
                return redirect('iniciar_sesion')
        except Estudiantes.DoesNotExist:
            messages.info(request, 'Usuario no existente')
            return redirect('iniciar_sesion')

def home_estudiante(request, documento):
    """
    Vista para mostrar la página principal del estudiante, en esta se puede hacer update
    de los datos del estudiante, cambiar la contraseña y hacer uso del menú de opciones que está
    en la barra de navegación.

    :param request: HttpRequest
    :param documento: str, documento del estudiante que está actualmente en sesión
    :return: HttpResponse, interfaz de la página principal del estudiante
    """
    estudiante = Estudiantes.objects.get(documento_identidad=documento)
    if request.method == 'GET':
        return render(request, 'Estudiantes/estudiante.html', {
            'estudiante': estudiante,
            'title': 'Home',
        })
    else:
        estudiante.update(nombre_completo=request.POST['nombre_completo'], documento_identidad=request.POST['documento'], programa_academico=request.POST['programa_academico'])
        messages.success(request, 'Datos modificados con éxito')
        return redirect('principal_estudiante', documento=estudiante.documento_identidad)

def get_clases(request,documento):
    """
    Vista para mostrar las clases que tiene el estudiante. En esta vista se puede ver y eliminar las clases que
    tiene el estudiante registradas en el sistema. Es decir, se ve y elimina los registros hechos por el estudiante,
    los cuales están en la tabla Registros.

    :param request: HttpRequest
    :param documento: str, documento del estudiante que está actualmente en sesión
    :return: HttpResponse, interfaz de las clases registradas por el estudiante
    """
    current_year = datetime.now().year
    estudiante = Estudiantes.objects.get(documento_identidad=documento)
    registros = Registros.objects(Q(codigo_estudiante=estudiante.id_estudiante) & Q(fecha_registro__gte=datetime(current_year, 1, 1), fecha_registro__lt=datetime(current_year, 12, 31)))
    clases = Clases.objects(id_clase__in=registros.distinct('id_clase'))
    if request.method == 'GET':
        return render(request, 'Estudiantes/clases.html', {
            'title': f'Clases {estudiante.nombre_completo}',
            'estudiante': estudiante,
            'clases': clases,
        })
    else:
        '''
        clase = request.POST['id_clase']
        registro = Registros.objects(Q(id_clase=clase) & Q(codigo_estudiante=estudiante.id_estudiante) & Q(fecha_registro__gte=datetime(current_year, 1, 1), fecha_registro__lt=datetime(current_year, 12, 31)))
        clase = Clases.objects.get(id_clase=clase)
        materia = Materias.objects.get(nombre_materia=clase.materia)
        reg = 0
        for cosa in registro:
            reg = cosa
        factura = Facturas.objects.get(id_factura=reg.id_factura)
        factura.update(valor=(factura.valor - (materia.numero_creditos * 725000)))
        registro.delete()
        messages.success(request, 'Materia eliminada con éxito')
        '''
        return redirect('clases_estudiante', documento=estudiante.documento_identidad)