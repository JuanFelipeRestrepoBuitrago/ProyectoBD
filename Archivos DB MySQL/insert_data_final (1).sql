USE matriculas_eafit;

-- Insertar estudiantes
INSERT INTO estudiantes (documento_identidad, programa_academico, nombre_completo, contraseña)
VALUES (1118133436, 'Ingeniería de Producción', 'Alejandro Gomez Castro', 'Alejo1'),
	   (2038488132, 'Ingeniería Mecánica', 'Valentina Castro Valencia', 'Valen2a'),
       (1246591872, 'Ecología', 'María Fernanda Rojas Garcia', 'Maria1a'),
       (1947700718, 'Comunicación Social', 'Pedro Perez Gonzalez', 'Pedropg'),
       (1863570766, 'Negocios Internacionales', 'Luis Vargas Gutierrez', '123'),
       (1725969593, 'Psicología', 'Diego Cadavid Seguro', 'Dieguito'),
       (2066860668, 'Música', 'David Herrera Gutierrez', 'Panitas123'),
       (2078764748, 'Literatura', 'Andres Valencia Buitrago', 'Poiuyt'),
       (1426015074, 'Diseño Urbano', 'Camilo Garcia Giraldo', 'Cami123'),
       (2003277789, 'Ingeniería de Sistemas', 'Andres Yepes Gonzalez', 'Andrew123');
       
-- Insertar materias
INSERT INTO materias (nombre_materia, numero_creditos)
VALUES ('Cálculo I', 2), ('Cálculo II', 2), ('Cálculo III', 3), ('Fundamentos de Programación', 3),
	   ('Física I', 3), ('Física II', 4), ('Prácticas Textuales', 3), ('Estructura de Datos I', 5),
       ('Estadística', 1), ('Ecología', 1), ('Lógica', 2), ('Estructuras Discretas', 3), ('Economía', 2),
       ('Contaduría I', 3), ('Procesos Contables', 4), ('Algebra Lineal', 15), ('Lenguajes Formales y Compiladores', 3);

-- Insertar profesores
INSERT INTO profesores (documento, certificaciones, nombre_completo)
VALUES (2059138408, 'Ingeniero de Software', 'Miguel Herrera Garcia'),
	   (1172904439, 'Matemático', 'David Castro Lopez'),
       (1442858283, 'Doctor en Literatura', 'Diego Restrepo Cardona'),
       (1092315440, 'Master en Finanzas', 'Sofia Restrepo Herrera'),
       (1198378094, 'Diseñador Gráfico', 'Javier Lopez Yepes'),
       (1454131828, 'Físico', 'Andres Restrepo Perez'),
       (1341881971, 'Doctor en Administración de Empresas', 'Nicolas Torres Vivero'),
       (1402478803, 'Abogado', 'Diego Vargas Vargas'),
       (1135566280, 'Ingeniero Ambiental', 'David Diaz Vivero'),
       (1117088410, 'Master en Inteligencia Artificial', 'Luis Rojas Hernandez');
       
-- Insertar aulas
INSERT INTO aulas (numero_bloque, numero_aula, capacidad, sede, tipo_aula)
VALUES (33, 402, 30, 'Poblado', 'Clase'), (13, 201, 15, 'Poblado', 'Laboratorio'), (18, 402, 23, 'Poblado', 'Computadores'),
	   (19, 201, 9, 'Poblado', 'Electrónica'), (13, 103, 5, 'Poblado', 'Química'), (19, 103, 18, 'Poblado', 'Mecánica'),
       (27, 304, 2, 'Poblado', 'Musical'), (38, 304, 25, 'Poblado', 'Clase'), (35, 401, 40, 'Poblado', 'Clase'), 
       (7, 101, 50, 'Poblado', 'Clase');

-- Insertar materias aprobadas     
INSERT INTO materias_aprobadas (codigo_estudiante, id_materia)
VALUES (1, 1), (1, 2), (1, 3), (2, 5), (2, 6), (4, 7), (3, 10), (8, 7), (10, 8), (10, 11), (10, 4), (10, 9), (5, 13);

-- Insertar materias prerrequisito
INSERT INTO materias_prerrequisito (id_materia, id_materia_prerrequisito)
VALUES (2, 1), (3, 2), (6, 5), (8, 4), (12, 11), (4, 11), (14, 13), (15, 14), (16, 9), (17, 12); 
       
-- Insertar las clases o cursos a dictar
INSERT INTO clases (tipo_clase, id_profesor, id_materia, horario, id_aula)
VALUES ('Magistral', 2, 1, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Martes", "Hora": "03:00:00 PM", "Duracion":"01:30:00"}, {"Dia": "Viernes", "Hora": "10:30:00 AM", "Duracion":"01:30:00"}]}', 1),
	   ('Magistral', 2, 2, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Martes", "Hora": "12:00:00 PM", "Duracion":"01:30:00"}, {"Dia": "Jueves", "Hora": "10:30:00 AM", "Duracion":"01:30:00"}]}', 2),
       ('Clase', NULL, 11, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Martes", "Hora": "06:00:00 AM", "Duracion":"01:30:00"}, {"Dia": "Miercoles", "Hora": "07:30:00 AM", "Duracion":"01:30:00"}]}', 3),
       ('Laboratorio', 6, 5, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Martes", "Hora": "04:00:00 PM", "Duracion":"02:00:00"}]}', NULL),
       ('Taller', 1, 12, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Lunes", "Hora": "10:00:00 AM", "Duracion":"02:00:00"}]}', 4),
       ('Clase', 2, 6, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Lunes", "Hora": "09:00:00 AM", "Duracion":"03:00:00"}]}', 5),
       ('Magistral', NULL, 3, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Lunes", "Hora": "04:30:00 PM", "Duracion":"01:30:00"}, {"Dia": "Jueves", "Hora": "04:30:00 PM", "Duracion":"01:30:00"}]}', NULL),
       ('Laboratorio', 2, 6, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Miercoles", "Hora": "09:00:00 AM", "Duracion":"02:00:00"}]}', 6),
       ('Clase', 1, 4, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Martes", "Hora": "10:30:00 AM", "Duracion":"01:30:00"}, {"Dia": "Jueves", "Hora": "12:00:00 PM", "Duracion":"01:30:00"}]}', 7),
       ('Clase', 3, 7, '{"Año": 2023, "Semestre": 1, "Horarios": [{"Dia": "Martes", "Hora": "6:00:00 PM", "Duracion":"03:00:00"}]}', 8);
       
-- Insertar las facturas
INSERT INTO facturas (pagado)
VALUES (0), (1), (0), (0), (0), (1), (0), (0), (0), (0);
--  DATE_ADD(CURDATE(), INTERVAL +2 MONTH),

-- Insertar registros de materias de estudiantes
INSERT INTO registros (codigo_estudiante, id_clase, id_factura)
VALUES (2, 1, 4), (2, 10, 4), (3, 1, 2), (3, 4, 2), (10, 5, 1),
	   (10, 1, 1), (10, 4, 1), (7, 10, 6), (5, 10, 3), (9, 10, 5);
       
INSERT INTO administradores
VALUES ('root', '123');
       
	
