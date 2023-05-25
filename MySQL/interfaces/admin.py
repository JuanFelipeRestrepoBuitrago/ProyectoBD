from django.contrib import admin
from .models import *

# Si se quiere hacer un CRUD de una tabla desde el apartado de administración de Django '/admin'
# se debe registrar el modelo en este archivo
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
