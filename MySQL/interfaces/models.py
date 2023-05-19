from django.db import models


# Create your models here.
class Estudiantes(models.Model):
    codigo_estudiante = models.AutoField(primary_key=True, db_comment='Id distintivo y ·nico que permite diferenciar a cada estudiante de la universidad.\n')
    documento_identidad = models.IntegerField(unique=True, db_comment='N·mero de documento ·nico que distingue a la persona seg·n la registraduria nacional, ademßs funge como usuario institucional.\n\n')
    programa_academico = models.CharField(max_length=100, db_comment='Es el programa academico en el cual estß inscrito el estudiante.\n')
    nombre_completo = models.CharField(max_length=120, db_comment='Nombre del estudiante tal cual aparece en su documento de identidad.\n')
    contraseña = models.CharField(max_length=30, db_comment='Contraseña con la cual el estudiante puede ingresar a la plataforma de matricula de materias.\n')

    class Meta:
        managed = False
        db_table = 'estudiantes'


class Facturas(models.Model):
    id_factura = models.AutoField(primary_key=True, db_comment='N·mero que identifica como ·nica a cada factura emitida.\n')
    fecha_emision = models.DateField(db_comment='Fecha que da constancia de cuando se emitio dicha factura.\n')
    fecha_vencimiento = models.DateField(blank=True, null=True, db_comment='Fecha que establece el plazo mßximo en el que se puede pagar la factura, esta es dos meses despuÚs de ser emitida.\n')
    pagado = models.IntegerField(db_comment='Valor boleano que identifica a una factura como paga.\n')
    valor = models.FloatField(blank=True, null=True, db_comment='Valor total de las materias matriculadas, es el precio que debe pagar la parsona.\n')

    class Meta:
        managed = False
        db_table = 'facturas'


class Profesores(models.Model):
    id_profesor = models.AutoField(primary_key=True, db_comment='Id distintivo y ·nico que permite diferenciar a cada profesor de la universidad.\n')
    nombre_completo = models.CharField(max_length=120, db_comment='Nombre del profesor tal cual aparece en su documento de identidad.\n')
    certificaciones = models.CharField(max_length=500, blank=True, null=True, db_comment='Documento o documentos que certifican al profesor en una o multiples areas de conocimiento.\n')
    documento = models.IntegerField(unique=True, db_comment='N·mero de documento ·nico que distingue a la persona seg·n la registraduria nacional\n')

    class Meta:
        managed = False
        db_table = 'profesores'


class Materias(models.Model):
    id_materia = models.AutoField(primary_key=True, db_comment='Id distintivo que distingue a cada materia, como ·nica.\n')
    nombre_materia = models.CharField(unique=True, max_length=100, db_comment='Nombre con el cual se identifica la materia de las demßs.\n')
    numero_creditos = models.IntegerField(db_comment='Es el n·mero de creditos totales con el que cuenta la materia, y representa el trabajo acßdemico que representa para el estudiante.\n')

    class Meta:
        managed = False
        db_table = 'materias'


class Aulas(models.Model):
    numero_bloque = models.PositiveIntegerField(primary_key=True, db_comment='Identificador del bloque, dentro de su respectiva sede, en el que se dictara la clase, en caso de ya estßr definido.\n')  # The composite primary key (numero_bloque, numero_aula) found, that is not supported. The first column is selected.
    numero_aula = models.PositiveIntegerField(db_comment='N·mero que identifica como ·nica a cada aula dentro de un bloque.\n')
    capacidad = models.IntegerField(db_comment='Aforo mßximo del aula.\n')
    sede = models.CharField(max_length=60, db_comment='Nombre de la sede de la universidad en la cual sse dictara la clase.\n')
    tipo_aula = models.CharField(max_length=12, blank=True, null=True, db_comment='El nombre identifica el tipo de sal¾n y con ello el tipo de clase que se puede dar en el.\n')

    class Meta:
        managed = False
        db_table = 'aulas'
        unique_together = (('numero_bloque', 'numero_aula'),)


class Administradores(models.Model):
    usuario = models.CharField(primary_key=True, max_length=30)
    contrasela = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'administradores'


class MateriasPrerrequisito(models.Model):
    id_materia = models.OneToOneField(Materias, models.DO_NOTHING, db_column='id_materia', primary_key=True, db_comment='Id de la materia que sirve como prerrequisito de la actual, la cual, si el estudiante no la ha aprovado no podra matricular la materia identificada por id_materia de la misma tabla.\n')  # The composite primary key (id_materia, id_materia_prerrequisito) found, that is not supported. The first column is selected.
    id_materia_prerrequisito = models.ForeignKey(Materias, models.DO_NOTHING, db_column='id_materia_prerrequisito', related_name='materiasprerrequisito_id_materia_prerrequisito_set', db_comment='Identificador unico de la materia.\n')

    class Meta:
        managed = False
        db_table = 'materias_prerrequisito'
        unique_together = (('id_materia', 'id_materia_prerrequisito'),)


class MateriasAprobadas(models.Model):
    codigo_estudiante = models.OneToOneField(Estudiantes, models.DO_NOTHING, db_column='codigo_estudiante', primary_key=True, db_comment='Id distintivo y ·nico que permite diferenciar a cada estudiante de la universidad que curso la y aprovo la materia.\n')  # The composite primary key (codigo_estudiante, id_materia) found, that is not supported. The first column is selected.
    id_materia = models.ForeignKey(Materias, models.DO_NOTHING, db_column='id_materia', db_comment='Id distintivo de la materia que curso y aprovo el estudiante.\n')

    class Meta:
        managed = False
        db_table = 'materias_aprobadas'
        unique_together = (('codigo_estudiante', 'id_materia'),)


class Clases(models.Model):
    id_clase = models.AutoField(primary_key=True, db_comment='Es el id ·nico con el cual se distinguen las multiples clases, que pueden llegar a haber en la universidad, tanto de otras materias como de la misma.\n')
    tipo_clase = models.CharField(max_length=11, db_comment='Identifica que tipo de actividades se harßn en cada clase, ya sea laboratorio, clase magistral, taller o clase convencional.\n')
    id_profesor = models.ForeignKey('Profesores', models.DO_NOTHING, db_column='id_profesor', blank=True, null=True, db_comment='Id del profesor asignado a la clase, en caso de este ya estar definido.\n')
    id_materia = models.ForeignKey('Materias', models.DO_NOTHING, db_column='id_materia', db_comment='Identificador unico de la materia de la cual se dicta la clase.\n')
    horario = models.JSONField(db_comment='Es el horario que tendrß asignada la clase en el dÝa o multiples dÝas que se dicte.\n')
    numero_bloque = models.ForeignKey(Aulas, models.DO_NOTHING, db_column='numero_bloque', blank=True, null=True, db_comment='Identificador del bloque, dentro de su respectiva sede, en el que se dictara la clase, en caso de ya estßr definido.\n')
    numero_aula = models.ForeignKey(Aulas, models.DO_NOTHING, db_column='numero_aula', to_field='numero_aula', related_name='clases_numero_aula_set', blank=True, null=True, db_comment='El n·mero del aula dentro del bloque que se dictara la clase, en caso de ya estar definido.\n')

    class Meta:
        managed = False
        db_table = 'clases'


class Registros(models.Model):
    codigo_estudiante = models.OneToOneField(Estudiantes, models.DO_NOTHING, db_column='codigo_estudiante', primary_key=True, db_comment='Codigo del estudiante que realiza el registro.\n')  # The composite primary key (codigo_estudiante, id_clase, fecha_registro) found, that is not supported. The first column is selected.
    id_clase = models.ForeignKey(Clases, models.DO_NOTHING, db_column='id_clase', db_comment='Identifica la clase registrada por el estudiante.\n')
    fecha_registro = models.DateField(db_comment='Identifica el la fecha en la cual se llevo a cabo el registro.\n')
    id_factura = models.ForeignKey(Facturas, models.DO_NOTHING, db_column='id_factura', db_comment='Identificador ·nico de la factura asociada a la transacci¾n.\n')

    class Meta:
        managed = False
        db_table = 'registros'
        unique_together = (('codigo_estudiante', 'id_clase', 'fecha_registro'),)