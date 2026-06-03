USE kaifer_db;

CREATE TABLE menu(

    id INT AUTO_INCREMENT PRIMARY KEY,
    plato VARCHAR(100) NOT NULL,
    precio INT NOT NULL,
    descripcion VARCHAR(150) NOT NULL,
    restricciones_alimenticias SET ('vegetariano', 'vegano', 'sin_lactosa', 'sin_gluten') NOT NULL  
);


CREATE TABLE usuarios (

    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    rol ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente'
);


CREATE TABLE resenas(
    id INT AUTO_INCREMENT PRIMARY KEY,
    contenido VARCHAR(200) NOT NULL,
    estrellas INT CHECK (estrellas BETWEEN 1 AND 5) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);


CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,   
    mesas INT NOT NULL CHECK (mesas BETWEEN 1 AND 30), -- maximo supuesto de 30 por el moemnto
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_reserva DATE NOT NULL,
    estado_reserva ENUM('pendiente', 'confirmada', 'cancelada') NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);

INSERT INTO usuarios (nombre, apellido, contrasena, email, rol) VALUES
('Gonzalo', 'Pereyra', '123', 'gg@gmail.com', 'cliente');

INSERT INTO menu (plato, precio, descripcion, restricciones_alimenticias) VALUES
('Milanesa con papas fritas', 500, 'Milanesa de carne vacuna acompañada de papas fritas crujientes.', 'vegetariano'),
('Ensalada César', 400, 'Ensalada fresca con lechuga, pollo a la parrilla, croutons y aderezo César.', 'sin_lactosa'),
('Pizza Margherita', 450, 'Pizza clásica con salsa de tomate, mozzarella y albahaca fresca.', 'vegano'),
('Hamburguesa Vegana', 550, 'Hamburguesa hecha con ingredientes vegetales, acompañada de papas al horno.', 'vegano,sin_lactosa');