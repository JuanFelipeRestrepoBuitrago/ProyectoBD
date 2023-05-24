from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='iniciar_sesion'),
    path('registrar/', registro_estudiante, name='registro_estudiante'),
    path('cambiar_contraseña/', cambiar_constraseña, name='cambiar_contraseña'),

    path('administracion/estudiantes/', view_estudiantes, name='view_estudiantes'),


    path('administracion/administradores/', crud_admin, name="crud_admin"),
    path('administracion/administradores/editar/<str:admin>', edit_admin, name="edit_admin"),
    path('administracion/administradores/crear', create_admin, name="create_admin"),
    path('administracion/profesores/', crud_profesores, name="crud_profesores"),
    path('administracion/profesores/editar/<int:profesor>', edit_profesores, name="edit_profe"),
    path('administracion/profesores/crear', create_profesores, name="create_profe"),
    path('administracion/materias/', crud_materias, name="crud_materias"),
    path('administracion/materias/editar/<int:materia>', edit_materias, name="edit_materia"),
    path('administracion/materias/crear', create_materias, name="create_materia"),
    path('administracion/materias/prerrequisitos', crud_materias_prerrequisito, name="crud_prerrequisitos"),
    path('administracion/materias/prerrequisitos/editar/<int:prerrequisito>', edit_materias_prerrequisito
         , name="edit_prerrequisito"),
    path('administracion/materias/prerrequisitos/crear', create_materias_prerrequisito, name="create_prerrequisito"),
    path('administracion/materias/aprobadas', crud_materias_aprobadas, name="crud_aprobadas"),
    path('administracion/materias/aprobadas/editar/<int:aprobada>', edit_materias_aprobadas, name="edit_aprobada"),
    path('administracion/materias/aprobadas/crear', create_materias_aprobadas, name="create_aprobada"),
    path('administracion/aulas/', crud_aulas, name="crud_aulas"),
    path('administracion/aulas/editar/<int:aula>', edit_aulas, name="edit_aula"),
    path('administracion/aulas/crear', create_aulas, name="create_aula"),
    path('administracion/clases/', crud_clases, name="crud_clases"),
    path('administracion/clases/editar/<int:clase>', edit_clases, name="edit_clase"),
    path('administracion/clases/crear', create_clases, name="create_clase"),

    path('estudiante/<int:documento>', home_estudiante, name='principal_estudiante'),
    path('estudiante/<int:documento>/clases', get_clases, name='clases_estudiante'),
    path('estudiante/<int:documento>/registrar_materias', registrar_materias, name='registrar_materias'),
    path('estudiante/<int:documento>/facturas', facturas_estudiante, name='facturas_estudiante'),
]
