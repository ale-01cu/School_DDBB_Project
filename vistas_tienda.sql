CREATE OR REPLACE VIEW proveedor_telefono AS 
                        SELECT proveedor.id_proveedor, proveedor.nombre, STRING_AGG(proveedor_telef.telefono, ', ') AS telefonos
                        FROM proveedor
                        LEFT JOIN proveedor_telef ON proveedor.id_proveedor = proveedor_telef.id_prov
                        GROUP BY proveedor.id_proveedor, proveedor.nombre;



 CREATE OR REPLACE VIEW listar_productos AS SELECT * FROM producto ORDER BY id_producto DESC
                       


CREATE OR REPLACE VIEW listar_producto_detalle AS 
                       SELECT p.id_producto, p.nombre, p.descripcion, p.cant_stock, p.precio, p.imagen, p.categoria, p.id_proveedor, m.tamanio_pantalla, m.espacio, m.memoria_ram, eh.consumo 
                       FROM producto p 
                       LEFT JOIN componente_pc cp ON p.id_producto = cp.id_producto 
                       LEFT JOIN movil m ON p.id_producto = m.id_producto AND m.tamanio_pantalla IS NOT NULL 
                       LEFT JOIN equipo_hogar eh 
                       ON p.id_producto = eh.id_producto


CREATE OR REPLACE VIEW carrito AS SELECT * FROM cliente_producto


CREATE OR REPLACE VIEW max_cant_stock_productos AS
                        SELECT MAX(cant_stock) AS max_valor
                        FROM producto;
                       


CREATE OR REPLACE VIEW listar_pedidos AS
                        SELECT 
                        p.id_pedido, 
                        p.id_cliente,
                        c.nombre,
                        c.email, 
                        p.fecha_pedido, 
                        p.cantidad, 
                        p.estado,
                        p.info_contacto, 
                        p.dir_envio, 
                        pp.id_producto,
                        pr.nombre as nombre_producto  
                        FROM pedido p 
                        LEFT JOIN cliente c ON c.id_cliente = p.id_cliente
                        LEFT JOIN pedido_producto pp ON p.id_pedido = pp.id_pedido
                        LEFT JOIN producto pr ON pr.id_producto = pp.id_producto 
                       


CREATE OR REPLACE VIEW listar_confirmaciones AS
                        SELECT 
                        c.id_confirmacion,
						lp.id_pedido, 
                        lp.nombre as nombre_cliente, 
                        lp.fecha_pedido, 
                        lp.cantidad, 
                        lp.info_contacto, 
                        lp.dir_envio,
						lp.nombre_producto,
						id_trabajador, 
						le.nombre as nombre_empleado, 
						le.fecha_creado,  
						le.años_experiencia
						FROM confirmaciones c 
                        LEFT JOIN listar_pedidos lp ON lp.id_pedido = c.id_pedido
                        LEFT JOIN listar_empleados le ON le.id_trabajador = c.id_empleado
                       


CREATE OR REPLACE VIEW listar_ventas AS
                        SELECT  
                        i_v.id_venta,
                        l_c.*,
						ganancia(l_c.id_pedido) AS ganancia_total
                        FROM info_ventas i_v
                        LEFT JOIN listar_confirmaciones l_c ON l_c.id_confirmacion = i_v.id_confirmacion



                       CREATE OR REPLACE VIEW total_productos AS SELECT COUNT(*) FROM producto;




CREATE OR REPLACE VIEW clientes_y_trabajadores AS 
                        SELECT id_usuario, nombre, password FROM usuario
                        



CREATE OR REPLACE VIEW listar_clientes AS
                        SELECT nombre, email, estado, fecha_creado, id_cliente FROM cliente;
                        



CREATE OR REPLACE VIEW listar_empleados AS 
                        SELECT id_trabajador, nombre, email, fecha_creado, estado, salario, años_experiencia, id_jefe FROM trabajador
                        



CREATE OR REPLACE VIEW listar_perfiles AS 
                        SELECT 
                        p.id_perfil, 
                        u.nombre, 
                        u.email ,
                        u.fecha_creado ,
                        p.ci
                        FROM perfil_usuario p 
                        LEFT JOIN usuario u ON u.id_usuario = p.id_perfil
                        