DROP TABLE IF EXISTS usuarios;

CREATE TABLE IF NOT EXISTS usuarios (

    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente'
);

DROP TABLE IF EXISTS reservas;

CREATE TABLE IF NOT EXISTS reservas (
    id             INT          AUTO_INCREMENT PRIMARY KEY,
    cliente        INT          NOT NULL,   
    mesas          INT          NOT NULL NOT NULL CHECK (mesas BETWEEN 1 AND 30), -- maximo supuesto de 30 por el moemnto
    created_at      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    fecha_reserva  DATE         NOT NULL,
    calificacion   INT          NOT NULL CHECK (calificacion BETWEEN 1 AND 5),
    estado_reserva ENUM('pendiente', 'confirmada', 'cancelada') NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (cliente)        REFERENCES usuarios(id)   ON DELETE CASCADE,
);