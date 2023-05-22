from django.shortcuts import render, redirect
from .models import Estudiantes, Clases, Facturas, Registros
from django.http import HttpResponse
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
            messages.error(request, 'Las contraseñas no son iguales')
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
        messages.success(request, 'Datos modificados con éxito')
        return redirect('principal_estudiante', documento=estudiante.documento_identidad)


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


@transaction.atomic
def get_clases(request, documento):
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    registros = estudiante.registros_set.filter(fecha_registro__year=datetime.now().year)
    clases = Clases.objects.filter(id_clase__in=registros.values('id_clase'))
    if request.method == 'GET':
        return render(request, 'Estudiante/clases.html', {
            'title': f'Clases {estudiante.nombre_completo}',
            'estudiante': estudiante,
            'clases': clases,
        })
    else:
        clase = request.POST['id_clase']
        registro = registros.get(id_clase=clase)

        registro.delete()
        messages.success(request, 'Materia eliminada con éxito')
        return redirect('clases_estudiante', documento=estudiante.documento_identidad)


@transaction.atomic
def registrar_materias(request, documento):
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    clases = Clases.objects.exclude(id_clase__in=estudiante.registros_set.values('id_clase'))
    registro = Registros.objects.filter(fecha_registro=datetime.now().date(), codigo_estudiante=estudiante, id_factura__pagado=False).first()

    if request.method == 'GET':
        return render(request, 'Estudiante/registrar_materias.html', {
            'title': 'Registrar Materias',
            'estudiante': estudiante,
            'clases': clases,
        })
    else:
        clase = request.POST['id_clase']
        try:
            if registro is None:
                raise Facturas.DoesNotExist
            factura = Facturas.objects.get(id_factura=registro.id_factura_id)
        except Facturas.DoesNotExist:
            factura = Facturas.objects.create()

        registro = estudiante.registros_set.create(codigo_estudiante=estudiante, id_clase_id=clase, id_factura=factura)
        registro.save()
        messages.success(request, 'Materia registrada y factura generada con éxito')
        return redirect('clases_estudiante', documento=estudiante.documento_identidad)


@transaction.atomic
def facturas_estudiante(request, documento):
    estudiante = Estudiantes.objects.select_for_update().get(documento_identidad=documento)
    registros = estudiante.registros_set
    facturas = Facturas.objects.filter(id_factura__in=registros.values('id_factura'))
    if request.method == 'GET':
        return render(request, 'Estudiante/facturas.html', {
            'title': 'Facturas',
            'estudiante': estudiante,
            'facturas': facturas,
        })
    else:
        factura = request.POST['id_factura']
        pagado = request.POST['pagado']
        print(pagado)
        factura = facturas.get(id_factura=factura)
        factura.pagado = pagado
        factura.save()

        messages.success(request, 'Factura modificada con éxito')
        return redirect('facturas_estudiante', documento=estudiante.documento_identidad)
