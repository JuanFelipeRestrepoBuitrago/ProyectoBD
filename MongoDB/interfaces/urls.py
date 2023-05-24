from django.urls import path
from .views import *

urlpatterns = [
    path('', login, name='iniciar_sesion'),
]