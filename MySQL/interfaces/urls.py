from django.urls import path
from .views import *
urlpatterns = [
    path('', login, name='iniciar_sesion'),
    path('registrar/', registro_estudiante, name='registro_estudiante'),
    path('cambiar_contraseña/', cambiar_constraseña, name='cambiar_contraseña'),

    path('administracion/', administracion, name='administracion'),
    path('administracion/administradores/', crud_admin, name="crud_admin"),
    path('administracion/administradores/editar/<str:admin>', edit_admin, name="edit_admin"),
    path('administracion/administradores/crear', create_admin, name="create_admin"),
    path('administracion/profesores/', crud_profesores, name="crud_profesores"),
    path('administracion/profesores/editar/<int:profesor>', edit_profesores, name="edit_profe"),
    path('administracion/profesores/crear', create_profesores, name="create_profe"),

    path('estudiante/<int:documento>', home_estudiante, name='principal_estudiante'),
    path('estudiante/<int:documento>/clases', get_clases, name='clases_estudiante'),
    path('estudiante/<int:documento>/registrar_materias', registrar_materias, name='registrar_materias'),
    path('estudiante/<int:documento>/facturas', facturas_estudiante, name='facturas_estudiante'),
]