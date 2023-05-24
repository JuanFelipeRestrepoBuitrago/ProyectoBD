from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Estudiantes)
admin.site.register(Clases)
admin.site.register(Materias)
admin.site.register(Registros)
admin.site.register(Facturas)
admin.site.register(Administradores)