from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Estudiantes)
admin.site.register(Clases)
admin.site.register(Materias)
admin.site.register(Profesores)
admin.site.register(Administradores)
admin.site.register(Aulas)
admin.site.register(Facturas)
admin.site.register(MateriasAprobadas)
admin.site.register(MateriasPrerrequisito)
admin.site.register(Registros)
