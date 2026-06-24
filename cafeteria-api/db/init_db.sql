CREATE DATABASE IF NOT EXISTS KAIFER_DB;
USE KAIFER_DB;

DROP TABLE IF EXISTS resenas;
DROP TABLE IF EXISTS reservas;
DROP TABLE IF EXISTS menu;
DROP TABLE IF EXISTS usuarios;


CREATE TABLE IF NOT EXISTS menu(

    id INT AUTO_INCREMENT PRIMARY KEY,
    plato VARCHAR(100) NOT NULL,
    precio INT NOT NULL,
    descripcion VARCHAR(150) NOT NULL,
    restricciones_alimenticias SET ('vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten') NOT NULL  
);


CREATE TABLE IF NOT EXISTS usuarios (

    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente'
);


CREATE TABLE IF NOT EXISTS resenas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    contenido VARCHAR(200) NOT NULL,
    estrellas INT CHECK (estrellas BETWEEN 1 AND 5) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,   
    mesas INT NOT NULL CHECK (mesas BETWEEN 1 AND 30), -- maximo supuesto de 30 por el moemnto
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_reserva DATETIME NOT NULL,
    estado_reserva ENUM('pendiente', 'confirmada', 'cancelada') NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);