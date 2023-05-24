from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from datetime import datetime
from django.db import transaction, IntegrityError
from django.contrib import messages
import re


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
                messages.error(request, "Error verificación")
                return redirect('iniciar_sesion')
        except (Estudiantes.DoesNotExist, ValueError):
            try:
                administrador = Administradores.objects.get(usuario=usuario)
                if administrador.contraseña == contraseña:
                    return redirect('crud_admin')
                else:
                    messages.error(request, "Error de verificación")
                    return redirect('iniciar_sesion')
            except (Administradores.DoesNotExist, ValueError):
                messages.error(request, "Usuario no existente")
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
    registro = Registros.objects.filter(fecha_registro=datetime.now().date(), codigo_estudiante=estudiante,
                                        id_factura__pagado=False).first()

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
        factura = facturas.get(id_factura=factura)
        factura.pagado = pagado
        factura.save()

        messages.success(request, 'Factura modificada con éxito')
        return redirect('facturas_estudiante', documento=estudiante.documento_identidad)


@transaction.atomic
def view_estudiantes(request):
    estudiantes = Estudiantes.objects.all()

    return render(request, 'Administrador/solo_lectura/view_estudiantes.html', {
        'estudiantes': estudiantes,
        'tittle': 'Ver Estudiantes',
    })


@transaction.atomic
def view_registros(request):
    registros = Registros.objects.all()

    return render(request, 'Administrador/solo_lectura/view_registros.html', {
        'registros': registros,
        'tittle': 'Ver Registros'
    })


@transaction.atomic
def view_facturas(request):
    facturas = Facturas.objects.all()

    return render(request, 'Administrador/solo_lectura/view_facturas.html', {
        'facturas': facturas,
        'tittle': 'Ver Facturas'
    })


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
            if Estudiantes.objects.filter(documento_identidad=usuario).exists():
                raise Estudiantes.DoesNotExist
            Administradores.objects.create(usuario=usuario, contraseña=contraseña)
            messages.success(request, 'Administrador creado con éxito')
            return redirect('crud_admin')
        except IntegrityError:
            messages.info(request, 'El usuario ya existe')
            return redirect('crud_admin')
        except Estudiantes.DoesNotExist:
            messages.info(request, 'Un usuario estudiante con ese nombre de usuario ya existe')
            return redirect('crud_admin')


@transaction.atomic
def crud_profesores(request):
    profesores = Profesores.objects.all()
    if request.method == "GET":
        return render(request, 'Administrador/profesores/crud_profesores.html', {
            'profesores': profesores,
            'tittle': 'Profesores',
        })
    else:
        id_profesor = request.POST['id_profesor']
        profesor = Profesores.objects.get(id_profesor=id_profesor)
        profesor.delete()
        messages.success(request, 'Profesor eliminado con éxito')
        return redirect('crud_profesores')


@transaction.atomic
def edit_profesores(request, profesor):
    profesor = Profesores.objects.get(id_profesor=profesor)

    if request.method == "GET":
        return render(request, 'Administrador/profesores/edit_profesores.html', {
            'profesor': profesor,
            'tittle': 'Editar Profesor',
        })
    else:
        nombre_completo = request.POST['nombre_completo']
        certificaciones = request.POST['certificaciones']
        documento_identidad = request.POST['documento']

        try:
            profesor.nombre_completo = nombre_completo
            profesor.certificaciones = certificaciones
            profesor.documento = documento_identidad
            profesor.save()
            messages.success(request, 'Profesor editado con éxito')
            return redirect('crud_profesores')
        except IntegrityError:
            messages.info(request, 'El profesor con ese documento ya existe')
            return redirect('edit_profe', profesor=profesor.id_profesor)


@transaction.atomic
def create_profesores(request):
    nombre_completo = request.POST['nombre_completo']
    certificaciones = request.POST['certificaciones']
    documento_identidad = request.POST['documento']
    try:
        Profesores.objects.create(nombre_completo=nombre_completo, certificaciones=certificaciones,
                                  documento=documento_identidad)
        messages.success(request, 'Profesor creado con éxito')
        return redirect('crud_profesores')
    except IntegrityError:
        messages.info(request, 'El profesor con ese documento ya existe')
        return redirect('crud_profesores')


@transaction.atomic
def crud_materias(request):
    materias = Materias.objects.all()
    if request.method == "GET":
        return render(request, 'Administrador/materias/crud_materias.html', {
            'materias': materias,
            'tittle': 'Materias',
        })
    else:
        id_materia = request.POST['id_materia']
        materia = Materias.objects.get(id_materia=id_materia)
        materia.delete()
        messages.success(request, 'Materia eliminada con éxito')
        return redirect('crud_materias')


@transaction.atomic
def edit_materias(request, materia):
    materia = Materias.objects.get(id_materia=materia)

    if request.method == "GET":
        return render(request, 'Administrador/materias/edit_materias.html', {
            'materia': materia,
            'tittle': 'Editar Materia',
        })
    else:
        nombre_materia = request.POST['nombre']
        numero_creditos = request.POST['creditos']
        try:
            materia.nombre_materia = nombre_materia
            materia.numero_creditos = numero_creditos
            materia.save()
            messages.success(request, 'Materia editada con éxito')
            return redirect('crud_materias')
        except IntegrityError:
            messages.info(request, 'La materia con ese nombre ya existe')
            return redirect('edit_materias', materia=materia.id_materia)


@transaction.atomic
def create_materias(request):
    nombre_materia = request.POST['nombre']
    numero_creditos = request.POST['creditos']
    try:
        Materias.objects.create(nombre_materia=nombre_materia, numero_creditos=numero_creditos)
        messages.success(request, 'Materia creada con éxito')
        return redirect('crud_materias')
    except IntegrityError:
        messages.info(request, 'La materia con ese nombre ya existe')
        return redirect('crud_materias')


@transaction.atomic
def crud_materias_prerrequisito(request):
    materias_prerrequisito = MateriasPrerrequisito.objects.all()
    materias = Materias.objects.all()

    if request.method == "GET":
        return render(request, 'Administrador/materias/prerrequisitos/crud_prerrequisitos.html', {
            'materias_prerrequisito': materias_prerrequisito,
            'tittle': 'Materias Prerrequisito',
            'materias': materias,
        })
    else:
        id_materia_prerrequisito = request.POST['id_materia_prerrequisito']
        materia_prerrequisito = MateriasPrerrequisito.objects.get(id_prerrequisito=id_materia_prerrequisito)
        materia_prerrequisito.delete()
        messages.success(request, 'Materia Prerrequisito eliminada con éxito')
        return redirect('crud_prerrequisitos')


@transaction.atomic
def edit_materias_prerrequisito(request, prerrequisito):
    materia_prerrequisito = MateriasPrerrequisito.objects.get(id_prerrequisito=prerrequisito)
    materias = Materias.objects.all()

    if request.method == "GET":
        return render(request, 'Administrador/materias/prerrequisitos/edit_prerrequisito.html', {
            'materia_prerrequisito': materia_prerrequisito,
            'tittle': 'Editar Materia Prerrequisito',
            'materias': materias,
        })
    else:
        nombre_materia = request.POST['materia']
        nombre_prerrequisito = request.POST['prerrequisito']

        try:
            materia_prerrequisito.id_materia_id = materias.get(nombre_materia=nombre_materia).id_materia
            materia_prerrequisito.id_materia_prerrequisito_id = materias.get(
                nombre_materia=nombre_prerrequisito).id_materia

            if nombre_materia == nombre_prerrequisito:
                messages.error(request, 'La materia y el prerrequisito no pueden ser iguales')
                return redirect('edit_prerrequisito', prerrequisito=materia_prerrequisito.id_prerrequisito)
            materia_prerrequisito.save()
            messages.success(request, 'Materia Prerrequisito editada con éxito')
            return redirect('crud_prerrequisitos')
        except IntegrityError:
            messages.info(request, 'La materia prerrequisito ya existe')
            return redirect('edit_prerrequisito', prerrequisito=materia_prerrequisito.id_prerrequisito)
        except Materias.DoesNotExist:
            messages.info(request, 'La materia o el prerrequisito no existen')
            return redirect('edit_prerrequisito', prerrequisito=materia_prerrequisito.id_prerrequisito)


@transaction.atomic
def create_materias_prerrequisito(request):
    materias = Materias.objects.all()
    nombre_materia = request.POST['materia']
    nombre_prerrequisito = request.POST['prerrequisito']

    try:
        if nombre_prerrequisito == nombre_materia:
            messages.error(request, 'La materia y el prerrequisito no pueden ser iguales')
            return redirect('crud_prerrequisitos')
        MateriasPrerrequisito.objects.create(id_materia_id=materias.get(nombre_materia=nombre_materia).id_materia,
                                             id_materia_prerrequisito_id=materias.get(
                                                 nombre_materia=nombre_prerrequisito).id_materia)
        messages.success(request, 'Materia Prerrequisito creada con éxito')
        return redirect('crud_prerrequisitos')
    except IntegrityError:
        messages.info(request, 'La materia prerrequisito ya existe')
        return redirect('crud_prerrequisitos')
    except Materias.DoesNotExist:
        messages.info(request, 'La materia o el prerrequisito no existen')
        return redirect('crud_prerrequisitos')


@transaction.atomic
def crud_materias_aprobadas(request):
    materias_aprobadas = MateriasAprobadas.objects.all()
    materias = Materias.objects.all()
    estudiantes = Estudiantes.objects.all()

    if request.method == "GET":
        return render(request, 'Administrador/materias/aprobadas/crud_aprobadas.html', {
            'materias_aprobadas': materias_aprobadas,
            'tittle': 'Materias Aprobadas',
            'materias': materias,
            'estudiantes': estudiantes,
        })
    else:
        id_materia_aprobada = request.POST['id_materia_aprobada']
        materia_aprobada = MateriasAprobadas.objects.get(id_materia_aprobada=id_materia_aprobada)
        materia_aprobada.delete()
        messages.success(request, 'Materia Aprobada eliminada con éxito')
        return redirect('crud_aprobadas')


@transaction.atomic
def edit_materias_aprobadas(request, aprobada):
    materia_aprobada = MateriasAprobadas.objects.get(id_materia_aprobada=aprobada)
    materias = Materias.objects.all()
    estudiantes = Estudiantes.objects.all()

    if request.method == "GET":
        return render(request, 'Administrador/materias/aprobadas/edit_aprobadas.html', {
            'materia_aprobada': materia_aprobada,
            'tittle': 'Editar Materia Aprobada',
            'materias': materias,
            'estudiantes': estudiantes,
        })
    else:
        nombre_materia = request.POST['materia']
        documento_estudiante = request.POST['estudiante']

        try:
            materia_aprobada.id_materia_id = materias.get(nombre_materia=nombre_materia).id_materia
            materia_aprobada.codigo_estudiante_id = estudiantes.get(
                documento_identidad=documento_estudiante).codigo_estudiante
            materia_aprobada.save()
            messages.success(request, 'Materia Aprobada editada con éxito')
            return redirect('crud_aprobadas')
        except IntegrityError:
            messages.info(request, 'La materia aprobada ya existe')
            return redirect('edit_aprobada', aprobada=materia_aprobada.id_materia_aprobada)
        except (Materias.DoesNotExist, Estudiantes.DoesNotExist):
            messages.info(request, 'La materia o el estudiante no existen')
            return redirect('edit_aprobada', aprobada=materia_aprobada.id_materia_aprobada)


@transaction.atomic
def create_materias_aprobadas(request):
    nombre_materia = request.POST['materia']
    documento = request.POST['estudiante']

    try:
        MateriasAprobadas.objects.create(id_materia_id=Materias.objects.get(nombre_materia=nombre_materia).id_materia,
                                         codigo_estudiante_id=Estudiantes.objects.get(
                                             documento_identidad=documento).codigo_estudiante)
        messages.success(request, 'Materia Aprobada creada con éxito')
        return redirect('crud_aprobadas')
    except IntegrityError:
        messages.info(request, 'La materia aprobada ya existe')
        return redirect('crud_aprobadas')
    except (Materias.DoesNotExist, Estudiantes.DoesNotExist):
        messages.info(request, 'La materia o el estudiante no existen')
        return redirect('crud_aprobadas')


@transaction.atomic
def crud_aulas(request):
    aulas = Aulas.objects.all()
    if request.method == "GET":
        return render(request, 'Administrador/aulas/crud_aulas.html', {
            'aulas': aulas,
            'tittle': 'Aulas',
            'tipos_aulas': ("Clase", 'Laboratorio', 'Química', 'Computadores', 'Electrónica', 'Mecánica', 'Musical'),
        })
    else:
        id_aula = request.POST['id_aula']
        aula = Aulas.objects.get(id_aula=id_aula)
        aula.delete()
        messages.success(request, 'Aula eliminada con éxito')
        return redirect('crud_aulas')


@transaction.atomic
def edit_aulas(request, aula):
    aula = Aulas.objects.get(id_aula=aula)
    if request.method == "GET":
        return render(request, 'Administrador/aulas/edit_aulas.html', {
            'aula': aula,
            'tittle': 'Editar Aula',
            'tipos_aulas': ("Clase", 'Laboratorio', 'Química', 'Computadores', 'Electrónica', 'Mecánica', 'Musical'),
        })
    else:
        numero_bloque = request.POST['numero_bloque']
        numero_aula = request.POST['numero_aula']
        capacidad = request.POST['capacidad']
        sede = request.POST['sede']
        if request.POST['tipo_aula'] == '':
            tipo_aula = None
        else:
            tipo_aula = request.POST['tipo_aula']

        try:
            aula.numero_bloque = numero_bloque
            aula.numero_aula = numero_aula
            aula.capacidad = capacidad
            aula.sede = sede
            aula.tipo_aula = tipo_aula
            aula.save()
            messages.success(request, 'Aula editada con éxito')
            return redirect('crud_aulas')
        except IntegrityError:
            messages.info(request, 'El aula ya existe')
            return redirect('edit_aula', aula=aula.id_aula)


@transaction.atomic
def create_aulas(request):
    numero_bloque = request.POST['numero_bloque']
    numero_aula = request.POST['numero_aula']
    capacidad = request.POST['capacidad']
    sede = request.POST['sede']
    if request.POST['tipo_aula'] == '':
        tipo_aula = None
    else:
        tipo_aula = request.POST['tipo_aula']

    try:
        Aulas.objects.create(numero_bloque=numero_bloque, numero_aula=numero_aula, capacidad=capacidad, sede=sede,
                             tipo_aula=tipo_aula)
        messages.success(request, 'Aula creada con éxito')
        return redirect('crud_aulas')
    except IntegrityError:
        messages.info(request, 'El aula ya existe')
        return redirect('crud_aulas')


@transaction.atomic
def crud_clases(request):
    clases = Clases.objects.all()
    profesores = Profesores.objects.all()
    materias = Materias.objects.all()
    aulas = Aulas.objects.all()

    if request.method == "GET":
        return render(request, 'Administrador/clases/crud_clases.html', {
            'clases': clases,
            'tittle': 'Clases',
            'tipos_clases': ("Clase", 'Laboratorio', 'Magistral', 'Taller'),
            'profesores': profesores,
            'materias': materias,
            'aulas': aulas,
        })
    else:
        id_clase = request.POST['id_clase']
        clase = Clases.objects.get(id_clase=id_clase)
        clase.delete()
        messages.success(request, 'Clase eliminada con éxito')
        return redirect('crud_clases')


@transaction.atomic
def edit_clases(request, clase):
    pattern_number = re.compile(r'^[0-9]+$')

    clase = Clases.objects.get(id_clase=clase)
    profesores = Profesores.objects.all()
    materias = Materias.objects.all()
    aulas = Aulas.objects.all()

    if request.method == "GET":
        return render(request, 'Administrador/clases/edit_clases.html', {
            'clase': clase,
            'tittle': 'Editar Clase',
            'tipos_clases': ("Clase", 'Laboratorio', 'Magistral', 'Taller'),
            'profesores': profesores,
            'materias': materias,
            'aulas': aulas,
        })
    else:
        tipo_clase = request.POST['tipo_clase']
        try:
            # profesor
            if request.POST['profesor'] == '':
                id_profesor = None
            else:
                if pattern_number.match(request.POST['profesor']):
                    id_profesor = Profesores.objects.get(id_profesor=request.POST['profesor']).id_profesor
                else:
                    messages.error(request, 'El profesor debe ser el id, no el nombre o documento')
                    return redirect('edit_clase', clase=clase.id_clase)

            # materia
            if pattern_number.match(request.POST['materia']):
                id_materia = Materias.objects.get(id_materia=request.POST['materia']).id_materia
            else:
                messages.error(request, 'La materia debe ser el id, no el nombre')
                return redirect('edit_clase', clase=clase.id_clase)

            # horario
            horario = request.POST['horario']

            # aula
            if request.POST['aula'] == '':
                id_aula = None
            else:
                if pattern_number.match(request.POST['aula']):
                    id_aula = Aulas.objects.get(id_aula=request.POST['aula']).id_aula
                else:
                    messages.error(request, 'El aula debe ser el id, no el bloque y número de aula')
                    return redirect('edit_clase', clase=clase.id_clase)
        except Profesores.DoesNotExist:
            messages.info(request, 'El profesor no existe')
            return redirect('edit_clase', clase=clase.id_clase)
        except Materias.DoesNotExist:
            messages.info(request, 'La materia no existe')
            return redirect('edit_clase', clase=clase.id_clase)
        except Aulas.DoesNotExist:
            messages.info(request, 'El aula no existe')
            return redirect('edit_clase', clase=clase.id_clase)

        try:
            clase.tipo_clase = tipo_clase
            clase.id_profesor_id = id_profesor
            clase.id_materia_id = id_materia
            clase.horario = horario
            clase.id_aula_id = id_aula
            clase.save()
            messages.success(request, 'Clase editada con éxito')
            return redirect('crud_clases')
        except Clases.DoesNotExist:
            messages.info(request, 'La clase no existe')
            return redirect('edit_clase', clase=clase.id_clase)


@transaction.atomic
def create_clases(request):
    pattern_number = re.compile(r'^[0-9]+$')
    tipo_clase = request.POST['tipo_clase']
    try:
        # profesor
        if request.POST['profesor'] == '':
            id_profesor = None
        else:
            if pattern_number.match(request.POST['profesor']):
                id_profesor = Profesores.objects.get(id_profesor=request.POST['profesor']).id_profesor
            else:
                messages.error(request, 'El profesor debe ser el id, no el nombre o documento')
                return redirect('crud_clases')

        # materia
        if pattern_number.match(request.POST['materia']):
            id_materia = Materias.objects.get(id_materia=request.POST['materia']).id_materia
        else:
            messages.error(request, 'La materia debe ser el id, no el nombre')
            return redirect('crud_clases')

        # horario
        horario = request.POST['horario']

        # aula
        if request.POST['aula'] == '':
            id_aula = None
        else:
            if pattern_number.match(request.POST['aula']):
                id_aula = Aulas.objects.get(id_aula=request.POST['aula']).id_aula
            else:
                messages.error(request, 'El aula debe ser el id, no el bloque y número de aula')
                return redirect('crud_clases')
    except Clases.DoesNotExist:
        messages.info(request, 'La clase no existe')
        return redirect('crud_clases')
    except Profesores.DoesNotExist:
        messages.info(request, 'El profesor no existe')
        return redirect('crud_clases')
    except Materias.DoesNotExist:
        messages.info(request, 'La materia no existe')
        return redirect('crud_clases')
    except Aulas.DoesNotExist:
        messages.info(request, 'El aula no existe')
        return redirect('crud_clases')

    try:
        Clases.objects.create(tipo_clase=tipo_clase, id_profesor_id=id_profesor, id_materia_id=id_materia,
                              horario=horario, id_aula_id=id_aula)
        messages.success(request, 'Clase creada con éxito')
        return redirect('crud_clases')
    except IntegrityError:
        messages.info(request, 'La clase ya existe')
        return redirect('crud_clases')
