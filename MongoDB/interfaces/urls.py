from django.urls import path
from .views import *

urlpatterns = [
    #URLS del apartado principal
    path('', login, name='iniciar_sesion'),
    path('registrar/', registro_estudiante, name='registro_estudiante'),
    path('cambiar_contraseña/', cambiar_constraseña, name='cambiar_contraseña'),

    #URLS del apartado de estudiantes
    path('estudiante/<int:documento>', home_estudiante, name='principal_estudiante'),
    path('estudiante/<int:documento>/clases', get_clases, name='clases_estudiante'),
    path('estudiante/<int:documento>/facturas', facturas_estudiante, name='facturas_estudiante'),
    # Llama a la vista registrar_materias
    path('estudiante/<int:documento>/registrar_materias', registrar_materias, name='registrar_materias'),

    #URLS del apartado de administradores
    path('administracion/administradores/', crud_admin, name="crud_admin"),
]