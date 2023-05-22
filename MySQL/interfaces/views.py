from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.db import transaction, IntegrityError
from django.contrib import messages


@transaction.atomic
def registro_estudiante(request):
    if request.method == "GET":
        return render(request, 'Principales/registro_estudiante.html', {
            'title': 'Registrar Estudiante',
        })
    else:
        documento = request.POST['documento']
        nombre = request.POST['nombre']
        programa_academico = request.POST['programa_academico']
        contraseña = request.POST['contraseña']
        contraseña_c = request.POST['contraseña_c']

        try:
            if contraseña != contraseña_c:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('registro_estudiante')
            Estudiantes.objects.create(documento_identidad=documento, nombre_completo=nombre,
                                       programa_academico=programa_academico, contraseña=contraseña)
            messages.success(request, 'Usuario creado con éxito')
            return redirect('iniciar_sesion')
        except ValueError:
            messages.error(request, 'Error al crear usuario')
            return redirect('registro_estudiante')
        except IntegrityError:
            messages.error(request, 'El usuario con ese documento ya existe')
            return redirect('registro_estudiante')


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


@transaction.atomic
def administracion(request):
    estudiantes = Estudiantes.objects.all()
    if request.method == "POST":
        codigo_estudiante = request.POST.get('codigo_estudiante')
        estudiante = Estudiantes.objects.get(codigo_estudiante=codigo_estudiante)
        estudiante.delete()
        return redirect('administracion')
    if request.method == 'PUT':
        return redirect('cu_estudiantes')
    return render(request, 'Administrador/crud_estudiantes.html', {'estudiantes': estudiantes, 'tittle': 'Admin'})


def crud_profesores(request):
    if request.method == "POST":
        if 'id_profesor' in request.POST:
            codigo_profesor = request.POST.get('id_profesor')
            profesor = Profesores.objects.get(id_profesor=codigo_profesor)
            profesor.delete()
        else:
            documento = request.POST.get('documento')
            certificaciones = request.POST.get('certificaciones')
            nombre = request.POST.get('nombre_completo')
            try:
                Profesores.objects.get(documento=documento)
                messages.error(request, "El profesor ya existe")
                return redirect('crud_profesores')
            except Profesores.DoesNotExist:
                profesor = Profesores.objects.create(documento=documento, certificaciones=certificaciones, nombre_completo=nombre)
                profesor.save()
                messages.success(request, "El profesor se guardó correctamente")
                return redirect('crud_profesores')

    profesores = Profesores.objects.all()
    return render(request, 'Administrador/crud_profesores.html', {'profesores': profesores, 'tittle': 'Admin'})


@transaction.atomic
def crud_admin(request):
    administradores = Administradores.objects.all()
    if request.method == "GET":
        return render(request, 'Administrador/administradores/crud_administrador.html', {
            'administradores': administradores,
            'tittle': 'Administradores',
        })
    else:
        id_admin = request.POST['id_admin']
        administrador = Administradores.objects.get(usuario=id_admin)
        administrador.delete()
        messages.success(request, 'Administrador eliminado con éxito')
        return redirect('crud_admin')


@transaction.atomic
def edit_admin(request, admin):
    admin = Administradores.objects.get(usuario=admin)

    if request.method == "GET":
        return render(request, 'Administrador/administradores/edit_admin.html', {
            'administrador': admin,
            'tittle': 'Editar Administrador',
        })
    else:
        contraseña = request.POST['contraseña']
        contraseña_c = request.POST['contraseña_confirmación']

        if contraseña != contraseña_c:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('edit_admin', admin=admin.usuario)
        admin.contraseña = contraseña
        admin.save()
        messages.success(request, 'Administrador editado con éxito')
        return redirect('crud_admin')


@transaction.atomic
def create_admin(request):
    usuario = request.POST['usuario']
    contraseña = request.POST['contraseña']
    contraseña_c = request.POST['contraseña_confirmación']

    if contraseña != contraseña_c:
        messages.error(request, 'Las contraseñas no coinciden')
        return redirect('crud_admin')
    else:
        try:
            Administradores.objects.create(usuario=usuario, contraseña=contraseña)
            messages.success(request, 'Administrador creado con éxito')
            return redirect('crud_admin')
        except IntegrityError:
            messages.info(request, 'El usuario ya existe')
            return redirect('crud_admin')

