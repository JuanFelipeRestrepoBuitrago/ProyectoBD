#from django.db import models
from djongo import models
from django import forms


class Clases(models.Model):
    tipo = models.CharField(max_length=20)
    profesor = models.JSONField(null=True)
    materia = models.CharField(max_length=30)
    aulas = models.JSONField(null=True)
    horario = models.JSONField(default={"Horario por asignar":0})

    class Meta:
        db_table = 'clases'

class Estudiantes(models.Model):
    documento_identidad = models.IntegerField()
    programa_academico = models.CharField(max_length=40)
    nombre_completo = models.CharField(max_length=70)
    contraseña = models.CharField(max_length=30)
    aprobadas = models.JSONField()

    class Meta:
        db_table = 'estudiantes'

class Materias(models.Model):
    nombre = models.CharField(max_length=40)
    numero_creditos = models.IntegerField()
    prerrequisitos = models.JSONField(null=True)

    class Meta:
        db_table = 'materias'

class Administradores(models.Model):
    usuario = models.IntegerField()
    contraseña = models.CharField(max_length=40)

    class Meta:
        db_table = 'admins'

class Registros(models.Model):
    codigo_estudiante = models.IntegerField()
    id_clase = models.IntegerField()
    fecha_registro = models.DateField()
    id_factura = models.IntegerField()

    class Meta:
        db_table = 'registros'

class Facturas(models.Model):
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    pagado = models.IntegerField(default=0)
    valor = models.FloatField(default=0)

    class Meta:
        db_table = 'facturas'





