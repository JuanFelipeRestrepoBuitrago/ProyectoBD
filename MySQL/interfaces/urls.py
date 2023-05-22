from django.urls import path
from .views import home_estudiante, get_clases, login, registro_estudiante, cambiar_constraseña, registrar_materias, facturas_estudiante

urlpatterns = [
    # Julio estas son las suyas
    path('', login, name='iniciar_sesion'),
    path('registrar/', registro_estudiante, name='registro_estudiante'),

    # Estas son las mias
    path('estudiante/<int:documento>', home_estudiante, name='principal_estudiante'),
    path('estudiante/<int:documento>/clases', get_clases, name='clases_estudiante'),
    path('estudiante/<int:documento>/registrar_materias', registrar_materias, name='registrar_materias'),
    path('estudiante/<int:documento>/facturas', facturas_estudiante, name='facturas_estudiante'),
    # aunque esta deberia ser parte de las tuyas, pero o hice yo
    path('cambiar_contraseña/', cambiar_constraseña, name='cambiar_contraseña'),
]