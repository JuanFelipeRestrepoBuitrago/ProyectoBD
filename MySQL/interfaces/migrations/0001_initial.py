# Generated by Django 4.2.1 on 2023-05-20 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administradores',
            fields=[
                ('usuario', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('contraseña', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'administradores',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Aulas',
            fields=[
                ('id_aula', models.AutoField(primary_key=True, serialize=False)),
                ('numero_bloque', models.PositiveIntegerField(db_comment='Identificador del bloque, dentro de su respectiva sede, en el que se dictara la clase, en caso de ya estßr definido.\n')),
                ('numero_aula', models.PositiveIntegerField(db_comment='N·mero que identifica como ·nica a cada aula dentro de un bloque.\n')),
                ('capacidad', models.IntegerField(db_comment='Aforo mßximo del aula.\n')),
                ('sede', models.CharField(db_comment='Nombre de la sede de la universidad en la cual sse dictara la clase.\n', max_length=60)),
                ('tipo_aula', models.CharField(blank=True, db_comment='El nombre identifica el tipo de sal¾n y con ello el tipo de clase que se puede dar en el.\n', max_length=12, null=True)),
            ],
            options={
                'db_table': 'aulas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Clases',
            fields=[
                ('id_clase', models.AutoField(db_comment='Es el id ·nico con el cual se distinguen las multiples clases, que pueden llegar a haber en la universidad, tanto de otras materias como de la misma.\n', primary_key=True, serialize=False)),
                ('tipo_clase', models.CharField(db_comment='Identifica que tipo de actividades se harßn en cada clase, ya sea laboratorio, clase magistral, taller o clase convencional.\n', max_length=11)),
                ('horario', models.JSONField(db_comment='Es el horario que tendrß asignada la clase en el dÝa o multiples dÝas que se dicte.\n')),
            ],
            options={
                'db_table': 'clases',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Estudiantes',
            fields=[
                ('codigo_estudiante', models.AutoField(db_comment='Id distintivo y ·nico que permite diferenciar a cada estudiante de la universidad.\n', primary_key=True, serialize=False)),
                ('documento_identidad', models.IntegerField(db_comment='N·mero de documento ·nico que distingue a la persona seg·n la registraduria nacional, ademßs funge como usuario institucional.\n\n', unique=True)),
                ('programa_academico', models.CharField(db_comment='Es el programa academico en el cual estß inscrito el estudiante.\n', max_length=100)),
                ('nombre_completo', models.CharField(db_comment='Nombre del estudiante tal cual aparece en su documento de identidad.\n', max_length=120)),
                ('contraseña', models.CharField(db_comment='Contrase±a con la cual el estudiante puede ingresar a la plataforma de matricula de materias.\n', max_length=30)),
            ],
            options={
                'db_table': 'estudiantes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Facturas',
            fields=[
                ('id_factura', models.AutoField(db_comment='N·mero que identifica como ·nica a cada factura emitida.\n', primary_key=True, serialize=False)),
                ('fecha_emision', models.DateField(db_comment='Fecha que da constancia de cuando se emitio dicha factura.\n')),
                ('fecha_vencimiento', models.DateField(blank=True, db_comment='Fecha que establece el plazo mßximo en el que se puede pagar la factura, esta es dos meses despuÚs de ser emitida.\n', null=True)),
                ('pagado', models.IntegerField(db_comment='Valor boleano que identifica a una factura como paga.\n')),
                ('valor', models.FloatField(blank=True, db_comment='Valor total de las materias matriculadas, es el precio que debe pagar la parsona.\n', null=True)),
            ],
            options={
                'db_table': 'facturas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Materias',
            fields=[
                ('id_materia', models.AutoField(db_comment='Id distintivo que distingue a cada materia, como ·nica.\n', primary_key=True, serialize=False)),
                ('nombre_materia', models.CharField(db_comment='Nombre con el cual se identifica la materia de las demßs.\n', max_length=100, unique=True)),
                ('numero_creditos', models.IntegerField(db_comment='Es el n·mero de creditos totales con el que cuenta la materia, y representa el trabajo acßdemico que representa para el estudiante.\n')),
            ],
            options={
                'db_table': 'materias',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MateriasAprobadas',
            fields=[
                ('id_materia_aprobada', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'materias_aprobadas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MateriasPrerrequisito',
            fields=[
                ('id_prerrequisito', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'materias_prerrequisito',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Profesores',
            fields=[
                ('id_profesor', models.AutoField(db_comment='Id distintivo y ·nico que permite diferenciar a cada profesor de la universidad.\n', primary_key=True, serialize=False)),
                ('nombre_completo', models.CharField(db_comment='Nombre del profesor tal cual aparece en su documento de identidad.\n', max_length=120)),
                ('certificaciones', models.CharField(blank=True, db_comment='Documento o documentos que certifican al profesor en una o multiples areas de conocimiento.\n', max_length=500, null=True)),
                ('documento', models.IntegerField(db_comment='N·mero de documento ·nico que distingue a la persona seg·n la registraduria nacional\n', unique=True)),
            ],
            options={
                'db_table': 'profesores',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Registros',
            fields=[
                ('id_registro', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_registro', models.DateField(db_comment='Identifica el la fecha en la cual se llevo a cabo el registro.\n')),
            ],
            options={
                'db_table': 'registros',
                'managed': False,
            },
        ),
    ]