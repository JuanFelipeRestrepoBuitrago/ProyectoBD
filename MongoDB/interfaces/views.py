from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError, models
from collections import OrderedDict
#from djongo import  models


# Create your views here.


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
    """
    Vista para mostrar la página principal del estudiante, en esta se puede hacer update
    de los datos del estudiante, cambiar la contraseña y hacer uso del menú de opciones que está
    en la barra de navegación.

    :param request: HttpRequest
    :param documento: str, documento del estudiante que está actualmente en sesión
    :return: HttpResponse, interfaz de la página principal del estudiante
    """
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


def get_clases(request,documento):
    """
    Vista para mostrar las clases que tiene el estudiante. En esta vista se puede ver y eliminar las clases que
    tiene el estudiante registradas en el sistema. Es decir, se ve y elimina los registros hechos por el estudiante,
    los cuales están en la tabla Registros.

    :param request: HttpRequest
    :param documento: str, documento del estudiante que está actualmente en sesión
    :return: HttpResponse, interfaz de las clases registradas por el estudiante
    """
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    registros = Registros.objects.filter(codigo_estudiante=estudiante.id, fecha_registro__year=datetime.now().year)
    clases = Clases.objects.filter(id__in=registros.values('id_clase'))
    if request.method == 'GET':
        return render(request, 'Estudiantes/clases.html', {
            'title': f'Clases {estudiante.nombre_completo}',
            'estudiante': estudiante,
            'clases': clases,
        })
    else:
        clase = request.POST['id_clase']
        registro = Registros.get(id_clase=clase)

        clase = Clases.objects.get(id=clase)
        materia = Materias.object.get(nombre=clase.materia)
        factura = Facturas.objects.get(id=registro.id_factura)
        factura.valor -= (materia.numero_creditos * 725.000)

        factura.save()
        registro.delete()
        messages.success(request, 'Materia eliminada con éxito')
        return redirect('clases_estudiante', documento=estudiante.documento_identidad)


def registrar_materias(request, documento):
    """
    Vista para que un estudiante pueda registrar clases. En esta vista se puede ver y registrar las clases que
    aún no ha registrado el estudiante en el sistema. Es decir, se crean los registro hechos por el estudiante,
    los cuales están en la tabla Registros.

    :param request: HttpRequest
    :param documento: str, documento del estudiante que está actualmente en sesión
    :return: HttpResponse, interfaz de las clases que aún no ha registrado el estudiante y que puede registrar
    """
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    registros = Registros.objects.filter(codigo_estudiante=estudiante.id)
    clases = Clases.objects.filter(~models.Q(id__in=registros.values('id_clase')))
    # clases = Clases.objects.exclude(id__in=registros.values('id_clase'))
    #clases = Clases.objects.filter(models.Q(id__in=registros.values('id_clase'))==False)
    facturas_no_pagadas = Facturas.objects.filter(pagado=False, id__in=registros.values('id_factura'))
    registro = Registros.objects.filter(fecha_registro=datetime.now().date(), codigo_estudiante=estudiante.id,
                                        id_factura__in=facturas_no_pagadas.values('id')).first()

    if request.method == 'GET':
        return render(request, 'Estudiantes/registrar_materias.html', {
            'title': 'Registrar Materias',
            'estudiante': estudiante,
            'clases': clases,
        })
    else:
        clase = request.POST['id_clase']
        try:
            if registro is None:
                raise Facturas.DoesNotExist
            factura = Facturas.objects.get(id_factura=registro.id_factura)
        except Facturas.DoesNotExist:
            factura = Facturas.objects.create(fecha_emision=datetime.now().date(), fecha_vencimiento=datetime.now().date())

        clase = Clases.objects.get(id=clase)
        materia = Materias.objects.get(nombre=clase.materia)
        factura.valor += (materia.numero_creditos * 725.000)
        registro = Registros.objects.create(codigo_estudiante=estudiante, id_clase=clase.id, id_factura=factura, fecha_registro=datetime.now().date())
        factura.save()
        registro.save()
        messages.success(request, 'Materia registrada y factura generada con éxito')
        return redirect('clases_estudiante', documento=estudiante.documento_identidad)


#Vista de las facturas para los diferentes estudiantes
def facturas_estudiante(request, documento):
    """
    Vista para que un estudiante pueda ver las facturas que tiene a su nombre. En esta vista se puede ver
    y solo se puede modificar el estado de la factura, es decir, si está pagada o no.

    :param request: HttpRequest
    :param documento: str, documento del estudiante que está actualmente en sesión
    :return: HttpResponse, interfaz de las facturas que tiene el estudiante a su nombre
    """
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    registros = Registros.objects.filter(codigo_estudiante=estudiante.id)
    facturas = Facturas.objects.filter(id__in=registros.values('id_factura'))
    if request.method == 'GET':
        return render(request, 'Estudiantes/facturas.html', {
            'title': 'Facturas',
            'estudiante': estudiante,
            'facturas': facturas,
        })
    else:
        factura = request.POST['id_factura']
        pagado = request.POST['pagado']
        factura = facturas.get(id_factura=factura)
        factura.pagado = pagado
        factura.save()

        messages.success(request, 'Factura modificada con éxito')
        return redirect('facturas_estudiante', documento=estudiante.documento_identidad)


def crud_admin(request):
    """
    Vista para hacer la crud de la tabla, administradores. En esta vista se puede crear, ver
    y eliminar administradores. Si se elige un administrador en específico, se redirige a una
    vista para editar el administrador seleccionado. Para crear un administrador se hace uso
    de la vista de crear administrador con un método POST.

    :param request: HttpRequest
    :return: HttpResponse, interfaz para la crud de la tabla, administradores
    """
    administradores = Administradores.objects.all()
    if request.method == "GET":
        return render(request, 'Administrador/crud_administradores.html', {
            'administradores': administradores,
            'tittle': 'Administradores',
        })
    else:
        id_admin = request.POST['id_admin']
        administrador = Administradores.objects.get(usuario=id_admin)
        administrador.delete()
        messages.success(request, 'Administrador eliminado con éxito')
        return redirect('crud_admin')

