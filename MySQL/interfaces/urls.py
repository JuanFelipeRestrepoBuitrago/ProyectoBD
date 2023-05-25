from django.urls import path
from .views import *

# Cada una de las rutas lleva a una vista diferente
urlpatterns = [
    # Llama a la vista login
    path('', login, name='iniciar_sesion'),
    # Llama a la vista registro_estudiante
    path('registrar/', registro_estudiante, name='registro_estudiante'),
    # Llama a la vista cambiar_contraseña
    path('cambiar_contraseña/', cambiar_constraseña, name='cambiar_contraseña'),

    # Llama a la vista view_estudiantes
    path('administracion/estudiantes/', view_estudiantes, name='view_estudiantes'),
    # Llama a la vista view_registros
    path('administracion/registros/', view_registros, name='view_registros'),
    # Llama a la vista view_facturas
    path('administracion/facturas/', view_facturas, name='view_facturas'),

    # Llama a la vista crud_administradores
    path('administracion/administradores/', crud_admin, name="crud_admin"),
    # Llama a la vista edit_administradores
    path('administracion/administradores/editar/<str:admin>', edit_admin, name="edit_admin"),
    # Llama a la vista create_administradores
    path('administracion/administradores/crear', create_admin, name="create_admin"),
    # Llama a la vista crud_profesores
    path('administracion/profesores/', crud_profesores, name="crud_profesores"),
    # Llama a la vista edit_profesores
    path('administracion/profesores/editar/<int:profesor>', edit_profesores, name="edit_profe"),
    # Llama a la vista create_profesores
    path('administracion/profesores/crear', create_profesores, name="create_profe"),
    # Llama a la vista crud_materias
    path('administracion/materias/', crud_materias, name="crud_materias"),
    # Llama a la vista edit_materias
    path('administracion/materias/editar/<int:materia>', edit_materias, name="edit_materia"),
    # Llama a la vista create_materias
    path('administracion/materias/crear', create_materias, name="create_materia"),
    # Llama a la vista crud_materias_prerrequisito
    path('administracion/materias/prerrequisitos', crud_materias_prerrequisito, name="crud_prerrequisitos"),
    # Llama a la vista edit_materias_prerrequisito
    path('administracion/materias/prerrequisitos/editar/<int:prerrequisito>', edit_materias_prerrequisito
         , name="edit_prerrequisito"),
    # Llama a la vista create_materias_prerrequisito
    path('administracion/materias/prerrequisitos/crear', create_materias_prerrequisito, name="create_prerrequisito"),
    # Llama a la vista crud_materias_aprobadas
    path('administracion/materias/aprobadas', crud_materias_aprobadas, name="crud_aprobadas"),
    # Llama a la vista edit_materias_aprobadas
    path('administracion/materias/aprobadas/editar/<int:aprobada>', edit_materias_aprobadas, name="edit_aprobada"),
    # Llama a la vista create_materias_aprobadas
    path('administracion/materias/aprobadas/crear', create_materias_aprobadas, name="create_aprobada"),
    # Llama a la vista crud_aulas
    path('administracion/aulas/', crud_aulas, name="crud_aulas"),
    # Llama a la vista edit_aulas
    path('administracion/aulas/editar/<int:aula>', edit_aulas, name="edit_aula"),
    # Llama a la vista create_aulas
    path('administracion/aulas/crear', create_aulas, name="create_aula"),
    # Llama a la vista crud_clases
    path('administracion/clases/', crud_clases, name="crud_clases"),
    # Llama a la vista edit_clases
    path('administracion/clases/editar/<int:clase>', edit_clases, name="edit_clase"),
    # Llama a la vista create_clases
    path('administracion/clases/crear', create_clases, name="create_clase"),

    # Llama a la vista home_estudiante
    path('estudiante/<int:documento>', home_estudiante, name='principal_estudiante'),
    # Llama a la vista get_clases
    path('estudiante/<int:documento>/clases', get_clases, name='clases_estudiante'),
    # Llama a la vista registrar_materias
    path('estudiante/<int:documento>/registrar_materias', registrar_materias, name='registrar_materias'),
    # Llama a la vista facturas_estudiante
    path('estudiante/<int:documento>/facturas', facturas_estudiante, name='facturas_estudiante'),
]
