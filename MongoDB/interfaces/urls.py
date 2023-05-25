from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='iniciar_sesion'),
    path('registrar/', registro_estudiante, name='registro_estudiante'),
    path('cambiar_contraseña/', cambiar_constraseña, name='cambiar_contraseña'),

    path('estudiante/<int:documento>', home_estudiante, name='principal_estudiante'),
    path('estudiante/<int:documento>/clases', get_clases, name='clases_estudiante'),
]