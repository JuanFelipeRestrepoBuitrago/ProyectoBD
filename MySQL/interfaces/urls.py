from django.urls import path
from .views import home_estudiante, get_clases, login, registro_estudiante, cambiar_constraseña

urlpatterns = [
    # Julio estas son las suyas
    path('', login, name='iniciar_sesion'),
    path('registrar/', registro_estudiante, name='registro_estudiante'),

    # Estas son las mias
    path('estudiante/<int:documento>', home_estudiante, name='principal_estudiante'),
    path('estudiante/<int:documento>/clases', get_clases, name='clases_estudiante'),
    # aunque esta deberia ser parte de las tuyas, pero o hice yo
    path('cambiar_contraseña/', cambiar_constraseña, name='cambiar_contraseña'),
]