from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='iniciar_sesion'),
    path('registrar/', registro_estudiante, name='registro_estudiante'),
]