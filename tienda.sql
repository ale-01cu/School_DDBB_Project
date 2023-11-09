CREATE TABLE proveedor(
	id_proveedor SERIAL PRIMARY KEY,
	nombre VARCHAR(50) NOT NULL
);

CREATE TABLE proveedor_telef(
	telefono VARCHAR(50) PRIMARY KEY,
	id_prov INT,
	FOREIGN KEY (id_prov) REFERENCES proveedor(id_proveedor) ON DELETE CASCADE
);


CREATE TABLE producto(
	id_producto SERIAL PRIMARY KEY,
	nombre VARCHAR(50) NOT NULL,
	descripcion TEXT,
	cant_stock INT NOT NULL,
	precio FLOAT NOT NULL,
	imagen VARCHAR(200),
	categoria VARCHAR(100) NOT NULL,
	id_proveedor INT,
	FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor) ON DELETE SET NULL

);

CREATE TABLE componente_pc(
	
) INHERITS (producto);


CREATE TABLE movil(
	tamanio_pantalla VARCHAR(10),
	espacio VARCHAR(10),
	memoria_ram VARCHAR(10)
) INHERITS (producto);


CREATE TABLE equipo_hogar(
	consumo VARCHAR(10)
) INHERITS (producto);


CREATE TABLE usuario(
	id_usuario SERIAL PRIMARY KEY,
	nombre VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(128) NOT NULL,
	fecha_creado DATE DEFAULT CURRENT_DATE,
	estado BOOLEAN DEFAULT TRUE
);


CREATE TABLE cliente(
	id_cliente SERIAL PRIMARY KEY

) INHERITS (usuario);


CREATE TABLE trabajador(
	id_trabajador SERIAL PRIMARY KEY,
	salario FLOAT NOT NULL,
	años_experiencia INT DEFAULT 0,
	id_jefe INT,
	FOREIGN KEY (id_jefe) REFERENCES trabajador(id_trabajador) ON DELETE SET NULL
	
) INHERITS (usuario);


CREATE TABLE cliente_producto(
	id_producto INT NOT NULL,
	id_cliente INT,
	--FOREIGN KEY (id_producto) REFERENCES producto(id_producto),
	FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
	PRIMARY KEY(id_producto, id_cliente)

);

CREATE TABLE pedido(
	id_pedido SERIAL PRIMARY KEY,
	id_cliente INT NOT NULL,
	fecha_pedido DATE DEFAULT CURRENT_DATE,
	cantidad INT DEFAULT 1,
	estado VARCHAR(50) NOT NULL DEFAULT 'PENDIENTE',
	info_contacto VARCHAR(255) NOT NULL,
	dir_envio VARCHAR(255) NOT NULL,
	FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE
);

CREATE TABLE pedido_producto(
	id_pedido INT,
	id_producto INT,
	FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
	PRIMARY KEY (id_pedido, id_producto)

);


CREATE TABLE confirmaciones(
	id_confirmacion SERIAL PRIMARY KEY,
	id_pedido INT,
	id_empleado INT,
	fecha_hora TIMESTAMP DEFAULT NOW(),
	FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
	FOREIGN KEY (id_empleado) REFERENCES trabajador(id_trabajador) ON DELETE CASCADE
);

CREATE TABLE info_ventas(
	id_venta SERIAL,
	id_pedido INT,
	id_confirmacion INT,
	FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE SET NULL,
	FOREIGN KEY (id_confirmacion) REFERENCES confirmaciones(id_confirmacion) ON DELETE SET NULL,
	PRIMARY KEY (id_venta, id_pedido, id_confirmacion)

);


CREATE TABLE perfil_usuario(
	id_perfil INT PRIMARY KEY,
	ci VARCHAR(255) DEFAULT ''
	--FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);


CREATE TABLE productos_vacios(
	id_producto INT,
	FOREIGN KEY(id_producto) REFERENCES producto(id_producto) ON DELETE SET NULL

)

CREATE TABLE historial_usuario(
	id_cliente INT,
	accion CHAR(255),
	fecha DATE DEFAULT CURRENT_DATE,
	FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente) ON DELETE SET NULL
)
                       

	
	
