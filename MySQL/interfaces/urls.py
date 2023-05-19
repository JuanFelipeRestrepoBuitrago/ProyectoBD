from django.urls import path
from .views import interfaz_eleccion, home_estudiante, get_clases, login, registro_estudiante

urlpatterns = [
    path('', interfaz_eleccion, name='interfaz_eleccion'),
    path('estudiante/<int:documento>', home_estudiante, name='home_estudiante'),
    path('estudiante/<int:documento>/clases', get_clases, name='get_clases'),

    path('registro/', registro_estudiante, name='registro_estudiante'),
    path('login/', login, name='login'),
]