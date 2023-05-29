from django.db import models
from mongoengine import Document,IntField,StringField,DictField,ListField,DateTimeField
from bson import ObjectId
import datetime

# Create your models here.
def fecha():
    fecha_actual = datetime.datetime.utcnow()
    nuevos_meses = fecha_actual.month + 2

    if nuevos_meses > 12:
        nuevos_meses = nuevos_meses % 12
        nuevos_años = fecha_actual.year + 1
    else:
        nuevos_años = fecha_actual.year

    nueva_fecha = fecha_actual.replace(year=nuevos_años, month=nuevos_meses)

    return nueva_fecha


class Estudiantes(Document):
    _id = ObjectId()
    id_estudiante = IntField()
    documento_identidad = IntField()
    programa_academico = StringField(max_length=40)
    nombre_completo = StringField(max_length=70)
    contraseña = StringField(max_length=30)
    aprobadas = ListField(StringField(), default=[])

    meta = {
        'db_alias': 'default',
        'collection': 'estudiantes'
    }

class Clases(Document):
    _id = ObjectId()
    id_clase = IntField()
    tipo_clase = StringField(max_length=30)
    profesor = DictField()
    materia = StringField(max_length=30)
    horario = StringField(max_length=250)
    aula = DictField()

    meta = {
        'db_alias': 'default',
        'collection' : 'clases'
    }

class Registros(Document):
    _id = ObjectId()
    id_registro = IntField()
    codigo_estudiante = IntField()
    id_clase = IntField()
    fecha_registro = DateTimeField(default=datetime.datetime.utcnow)
    id_factura = IntField()

    meta = {
        'db_alias': 'default',
        'collection': 'registros'
    }

class Materias(Document):
    _id = ObjectId()
    id_materia = IntField()
    nombre_materia = StringField(max_length=30)
    numero_creditos = IntField()
    prerequisitos = ListField(default=[])

    meta = {
        'db_alias': 'default',
        'collection': 'materias'
    }

class Facturas(Document):
    _id = ObjectId()
    id_factura = IntField()
    fecha_emision = DateTimeField(default=datetime.datetime.utcnow)
    fecha_vencimiento = DateTimeField(default=fecha())

    meta = {
        'db_alias': 'default',
        'collection': 'facturas'
    }