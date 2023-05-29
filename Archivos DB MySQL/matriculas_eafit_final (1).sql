-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema matriculas_eafit
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema matriculas_eafit
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `matriculas_eafit` DEFAULT CHARACTER SET utf8mb3 ;
USE `matriculas_eafit` ;

-- -----------------------------------------------------
-- Table `matriculas_eafit`.`materias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`materias` (
  `id_materia` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Id distintivo que distingue a cada materia, como única.\n',
  `nombre_materia` VARCHAR(100) NOT NULL COMMENT 'Nombre con el cual se identifica la materia de las demás.\n',
  `numero_creditos` INT NOT NULL COMMENT 'Es el número de creditos totales con el que cuenta la materia, y representa el trabajo acádemico que representa para el estudiante.\n',
  PRIMARY KEY (`id_materia`),
  UNIQUE INDEX `nombre_materia_UNIQUE` (`nombre_materia` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`profesores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`profesores` (
  `id_profesor` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Id distintivo y único que permite diferenciar a cada profesor de la universidad.\n',
  `nombre_completo` VARCHAR(120) NOT NULL COMMENT 'Nombre del profesor tal cual aparece en su documento de identidad.\n',
  `certificaciones` VARCHAR(500) NULL DEFAULT NULL COMMENT 'Documento o documentos que certifican al profesor en una o multiples areas de conocimiento.\n',
  `documento` INT NOT NULL COMMENT 'Número de documento único que distingue a la persona según la registraduria nacional\n',
  PRIMARY KEY (`id_profesor`),
  UNIQUE INDEX `documento_UNIQUE` (`documento` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`aulas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`aulas` (
  `id_aula` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `numero_bloque` INT UNSIGNED NOT NULL COMMENT 'Identificador del bloque, dentro de su respectiva sede, en el que se dictara la clase, en caso de ya estár definido.\n',
  `numero_aula` INT UNSIGNED NOT NULL COMMENT 'Número que identifica como única a cada aula dentro de un bloque.\n',
  `capacidad` INT NOT NULL COMMENT 'Aforo máximo del aula.\n',
  `sede` VARCHAR(60) NOT NULL COMMENT 'Nombre de la sede de la universidad en la cual sse dictara la clase.\n',
  `tipo_aula` ENUM('Clase', 'Laboratorio', 'Química', 'Computadores', 'Electrónica', 'Mecánica', 'Musical') NULL COMMENT 'El nombre identifica el tipo de salón y con ello el tipo de clase que se puede dar en el.\n',
  PRIMARY KEY (`id_aula`),
  UNIQUE INDEX `idx_bloque_aula` (`numero_bloque` ASC, `numero_aula` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`clases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`clases` (
  `id_clase` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Es el id único con el cual se distinguen las multiples clases, que pueden llegar a haber en la universidad, tanto de otras materias como de la misma.\n',
  `tipo_clase` ENUM('Clase', 'Laboratorio', 'Magistral', 'Taller') NOT NULL COMMENT 'Identifica que tipo de actividades se harán en cada clase, ya sea laboratorio, clase magistral, taller o clase convencional.\n',
  `id_profesor` INT UNSIGNED NULL COMMENT 'Id del profesor asignado a la clase, en caso de este ya estar definido.\n',
  `id_materia` INT UNSIGNED NOT NULL COMMENT 'Identificador unico de la materia de la cual se dicta la clase.\n',
  `horario` JSON NOT NULL COMMENT 'Es el horario que tendrá asignada la clase en el día o multiples días que se dicte.\n',
  `id_aula` INT UNSIGNED NULL,
  PRIMARY KEY (`id_clase`),
  INDEX `fk_clases_profesores1_idx` (`id_profesor` ASC) VISIBLE,
  INDEX `fk_clases_materias1_idx` (`id_materia` ASC) VISIBLE,
  INDEX `fk_clases_aulas1_idx` (`id_aula` ASC) VISIBLE,
  CONSTRAINT `fk_clases_materias1`
    FOREIGN KEY (`id_materia`)
    REFERENCES `matriculas_eafit`.`materias` (`id_materia`),
  CONSTRAINT `fk_clases_profesores1`
    FOREIGN KEY (`id_profesor`)
    REFERENCES `matriculas_eafit`.`profesores` (`id_profesor`),
  CONSTRAINT `fk_clases_aulas1`
    FOREIGN KEY (`id_aula`)
    REFERENCES `matriculas_eafit`.`aulas` (`id_aula`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`estudiantes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`estudiantes` (
  `codigo_estudiante` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Id distintivo y único que permite diferenciar a cada estudiante de la universidad.\n',
  `documento_identidad` INT NOT NULL COMMENT 'Número de documento único que distingue a la persona según la registraduria nacional, además funge como usuario institucional.\n\n',
  `programa_academico` VARCHAR(100) NOT NULL COMMENT 'Es el programa academico en el cual está inscrito el estudiante.\n',
  `nombre_completo` VARCHAR(120) NOT NULL COMMENT 'Nombre del estudiante tal cual aparece en su documento de identidad.\n',
  `contraseña` VARCHAR(30) NOT NULL COMMENT 'Contraseña con la cual el estudiante puede ingresar a la plataforma de matricula de materias.\n',
  PRIMARY KEY (`codigo_estudiante`),
  UNIQUE INDEX `documento_identidad_UNIQUE` (`documento_identidad` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`materias_aprobadas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`materias_aprobadas` (
  `id_materia_aprobada` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `codigo_estudiante` INT UNSIGNED NOT NULL,
  `id_materia` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_materia_aprobada`),
  INDEX `fk_materias_aprobadas_estudiantes1_idx` (`codigo_estudiante` ASC) VISIBLE,
  INDEX `fk_materias_aprobadas_materias1_idx` (`id_materia` ASC) VISIBLE,
  UNIQUE INDEX `idx_materia_estudiante` (`codigo_estudiante` ASC, `id_materia` ASC) VISIBLE,
  CONSTRAINT `fk_materias_aprobadas_estudiantes1`
    FOREIGN KEY (`codigo_estudiante`)
    REFERENCES `matriculas_eafit`.`estudiantes` (`codigo_estudiante`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_materias_aprobadas_materias1`
    FOREIGN KEY (`id_materia`)
    REFERENCES `matriculas_eafit`.`materias` (`id_materia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`facturas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`facturas` (
  `id_factura` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Número que identifica como única a cada factura emitida.\n',
  `fecha_emision` DATE NOT NULL COMMENT 'Fecha que da constancia de cuando se emitio dicha factura.\n',
  `fecha_vencimiento` DATE NOT NULL COMMENT 'Fecha que establece el plazo máximo en el que se puede pagar la factura, esta es dos meses después de ser emitida.\n',
  `pagado` TINYINT NOT NULL COMMENT 'Valor boleano que identifica a una factura como paga.\n',
  `valor` DOUBLE NULL DEFAULT 0.0 COMMENT 'Valor total de las materias matriculadas, es el precio que debe pagar la parsona.\n',
  PRIMARY KEY (`id_factura`, `fecha_emision`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`registros`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`registros` (
  `id_registro` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `codigo_estudiante` INT UNSIGNED NOT NULL COMMENT 'Codigo del estudiante que realiza el registro.\n',
  `id_clase` INT UNSIGNED NOT NULL COMMENT 'Identifica la clase registrada por el estudiante.\n',
  `fecha_registro` DATE NOT NULL COMMENT 'Identifica el la fecha en la cual se llevo a cabo el registro.\n',
  `id_factura` INT UNSIGNED NOT NULL COMMENT 'Identificador único de la factura asociada a la transacción.\n',
  INDEX `fk_estudiantes_has_clases_clases1_idx` (`id_clase` ASC) VISIBLE,
  INDEX `fk_estudiantes_has_clases_estudiantes1_idx` (`codigo_estudiante` ASC) VISIBLE,
  INDEX `fk_registros_facturas1_idx` (`id_factura` ASC) VISIBLE,
  PRIMARY KEY (`id_registro`),
  UNIQUE INDEX `idx_estudiante_clase_fecha` (`codigo_estudiante` ASC, `id_clase` ASC, `fecha_registro` ASC) VISIBLE,
  CONSTRAINT `fk_estudiantes_has_clases_estudiantes1`
    FOREIGN KEY (`codigo_estudiante`)
    REFERENCES `matriculas_eafit`.`estudiantes` (`codigo_estudiante`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_estudiantes_has_clases_clases1`
    FOREIGN KEY (`id_clase`)
    REFERENCES `matriculas_eafit`.`clases` (`id_clase`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_registros_facturas1`
    FOREIGN KEY (`id_factura`)
    REFERENCES `matriculas_eafit`.`facturas` (`id_factura`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`materias_prerrequisito`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`materias_prerrequisito` (
  `id_prerrequisito` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_materia` INT UNSIGNED NOT NULL,
  `id_materia_prerrequisito` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id_prerrequisito`),
  INDEX `fk_materias_prerrequisito_materias1_idx` (`id_materia` ASC) VISIBLE,
  INDEX `fk_materias_prerrequisito_materias2_idx` (`id_materia_prerrequisito` ASC) VISIBLE,
  UNIQUE INDEX `idx_materia_prerrequisito` (`id_materia` ASC, `id_materia_prerrequisito` ASC) VISIBLE,
  CONSTRAINT `fk_materias_prerrequisito_materias1`
    FOREIGN KEY (`id_materia`)
    REFERENCES `matriculas_eafit`.`materias` (`id_materia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_materias_prerrequisito_materias2`
    FOREIGN KEY (`id_materia_prerrequisito`)
    REFERENCES `matriculas_eafit`.`materias` (`id_materia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `matriculas_eafit`.`administradores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`administradores` (
  `usuario` VARCHAR(30) NOT NULL,
  `contraseña` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`usuario`))
ENGINE = InnoDB;

USE `matriculas_eafit` ;

-- -----------------------------------------------------
-- Placeholder table for view `matriculas_eafit`.`Materias Aprobadas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`Materias Aprobadas` (`Estudiante` INT, `Carrera` INT, `'Materias Aprobadas'` INT);

-- -----------------------------------------------------
-- Placeholder table for view `matriculas_eafit`.`Materias Prerrequisito`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`Materias Prerrequisito` (`Materia` INT, `Prerrequisito` INT);

-- -----------------------------------------------------
-- Placeholder table for view `matriculas_eafit`.`clase`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`clase` (`Materia` INT, `Profesor` INT, `Horario` INT, `Aula` INT);

-- -----------------------------------------------------
-- Placeholder table for view `matriculas_eafit`.`Registro de Materias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`Registro de Materias` (`Estudiante` INT, `'Fecha de Registro'` INT, `Valor` INT, `Clases` INT);

-- -----------------------------------------------------
-- Placeholder table for view `matriculas_eafit`.`Valor de las facturas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `matriculas_eafit`.`Valor de las facturas` (`'ID de la Factura'` INT, `Valor` INT);

-- -----------------------------------------------------
-- View `matriculas_eafit`.`Materias Aprobadas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `matriculas_eafit`.`Materias Aprobadas`;
USE `matriculas_eafit`;
CREATE  OR REPLACE VIEW `Materias Aprobadas` AS
SELECT e.nombre_completo AS Estudiante, e.programa_academico AS Carrera, GROUP_CONCAT(m.nombre_materia) AS 'Materias Aprobadas'
FROM materias_aprobadas AS ma
RIGHT JOIN estudiantes AS e ON e.codigo_estudiante = ma.codigo_estudiante
LEFT JOIN materias AS m ON m.id_materia = ma.id_materia
GROUP BY Estudiante, Carrera;

-- -----------------------------------------------------
-- View `matriculas_eafit`.`Materias Prerrequisito`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `matriculas_eafit`.`Materias Prerrequisito`;
USE `matriculas_eafit`;
CREATE  OR REPLACE VIEW `Materias Prerrequisito` AS
SELECT m.nombre_materia AS Materia, mp.nombre_materia AS Prerrequisito
FROM materias_prerrequisito AS mat_pre
INNER JOIN materias AS m ON m.id_materia = mat_pre.id_materia
INNER JOIN materias AS mp ON mp.id_materia = mat_pre.id_materia_prerrequisito;

-- -----------------------------------------------------
-- View `matriculas_eafit`.`clase`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `matriculas_eafit`.`clase`;
USE `matriculas_eafit`;
CREATE  OR REPLACE VIEW `clase` AS
SELECT CONCAT(m.nombre_materia, '-', c.id_clase) AS Materia, p.nombre_completo AS Profesor, c.horario AS Horario, CONCAT(a.numero_bloque, '-', a.numero_aula) AS Aula
FROM clases AS c
INNER JOIN materias AS m ON c.id_materia = m.id_materia
LEFT JOIN profesores AS p ON c.id_profesor = p.id_profesor
INNER JOIN aulas AS a ON a.id_aula = c.id_aula;

-- -----------------------------------------------------
-- View `matriculas_eafit`.`Registro de Materias`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `matriculas_eafit`.`Registro de Materias`;
USE `matriculas_eafit`;
CREATE  OR REPLACE VIEW `Registro de Materias` AS
SELECT e.nombre_completo AS Estudiante, r.fecha_registro AS 'Fecha de Registro', f.valor AS Valor,GROUP_CONCAT(CONCAT(m.nombre_materia, '-', c.id_clase)) AS Clases
FROM estudiantes AS e
INNER JOIN registros AS r ON r.codigo_estudiante = e.codigo_estudiante
INNER JOIN clases AS c ON c.id_clase = r.id_clase
INNER JOIN materias AS m ON c.id_materia = m.id_materia
INNER JOIN facturas AS f ON f.id_factura = r.id_factura
GROUP BY Estudiante, r.fecha_registro, Valor
ORDER BY Estudiante, r.fecha_registro, Valor;

-- -----------------------------------------------------
-- View `matriculas_eafit`.`Valor de las facturas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `matriculas_eafit`.`Valor de las facturas`;
USE `matriculas_eafit`;
CREATE  OR REPLACE VIEW `Valor de las facturas` AS
SELECT f.id_factura AS 'ID de la Factura', SUM(m.numero_creditos) * 725000 AS Valor
FROM facturas AS f
LEFT JOIN registros AS r ON r.id_factura = f.id_factura
LEFT JOIN clases AS c ON c.id_clase = r.id_clase
LEFT JOIN materias AS m ON m.id_materia = c.id_materia
GROUP BY f.id_factura
ORDER BY f.id_factura;
USE `matriculas_eafit`;

DELIMITER $$
USE `matriculas_eafit`$$
CREATE DEFINER = CURRENT_USER TRIGGER `matriculas_eafit`.`fecha_vencimiento` BEFORE INSERT ON `facturas` FOR EACH ROW
BEGIN
	SET NEW.fecha_emision = NOW();
	SET NEW.fecha_vencimiento = DATE_ADD(NEW.fecha_emision, INTERVAL +2 MONTH);
END$$

USE `matriculas_eafit`$$
CREATE DEFINER = CURRENT_USER TRIGGER `matriculas_eafit`.`fecha_registro` BEFORE INSERT ON `registros` FOR EACH ROW
BEGIN
	SET NEW.fecha_registro = NOW();
END$$

USE `matriculas_eafit`$$
CREATE DEFINER = CURRENT_USER TRIGGER `matriculas_eafit`.`valor_factura` AFTER INSERT ON `registros` FOR EACH ROW
BEGIN
	UPDATE facturas 
    SET valor = valor + (SELECT m.numero_creditos * 725000.0
		FROM registros AS r
		JOIN clases AS c ON c.id_clase = r.id_clase
		JOIN materias AS m ON c.id_materia = m.id_materia
		WHERE id_registro = NEW.id_registro)
    WHERE id_factura = NEW.id_factura;
END$$

USE `matriculas_eafit`$$
CREATE DEFINER = CURRENT_USER TRIGGER `matriculas_eafit`.`restar_factura` BEFORE DELETE ON `registros` FOR EACH ROW
BEGIN
	UPDATE facturas 
	SET valor = valor - (SELECT m.numero_creditos * 725000.0
		FROM registros AS r
		JOIN clases AS c ON c.id_clase = r.id_clase
		JOIN materias AS m ON c.id_materia = m.id_materia
		WHERE id_registro = OLD.id_registro)
    WHERE id_factura = OLD.id_factura;
END$$


DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
