from django.db import connection

def execute_functions():

    with connection.cursor() as cursor:
                                
        # Funciones
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION insertar_proveedor(nombre VARCHAR(50), telefono VARCHAR(50)) RETURNS proveedor AS
                        $$
                            DECLARE
                                resultado proveedor;
                                id_proveedor INTEGER;
                                el_proveedor proveedor;

                            BEGIN
                                SELECT * INTO el_proveedor FROM proveedor WHERE LOWER(proveedor.nombre) = LOWER(insertar_proveedor.nombre);
                                
                                IF FOUND THEN
                                    RAISE NOTICE 'estoy dentro del if';
                                    INSERT INTO proveedor_telef (id_prov, telefono) VALUES (el_proveedor.id_proveedor, telefono);
                                    RETURN el_proveedor;
                                END IF;
                                
                                RAISE NOTICE 'estoy fuera del if';
                                INSERT INTO proveedor (nombre) VALUES (nombre);
                                SELECT INTO id_proveedor currval(pg_get_serial_sequence('proveedor', 'id_proveedor'));
                                INSERT INTO proveedor_telef (id_prov, telefono) VALUES (id_proveedor, telefono);
                                SELECT * INTO resultado FROM proveedor_telefono WHERE telefono = insertar_proveedor.telefono;
                                RETURN resultado;
                            END
                        $$
                        LANGUAGE plpgsql;
                       
                       """)
        
        
        cursor.execute("""
                       
                       CREATE OR REPLACE FUNCTION eliminar_proveedor(id INTEGER) RETURNS SETOF proveedor AS
                       $$
                            DECLARE
                                resultado proveedor;
                                
                            BEGIN
                                SELECT * INTO resultado FROM proveedor WHERE id_proveedor = id;
                            
                                IF FOUND THEN
                                    DELETE FROM proveedor WHERE id_proveedor = id;
                                    SELECT * INTO resultado FROM proveedor WHERE id_proveedor = id;
                                    RETURN NEXT resultado;
                                END IF;        
                                
                                RETURN;
                                
                            END;
                       
                       $$
                       LANGUAGE plpgsql;
                       
                       """)
        
        
        cursor.execute("""
                       
                            CREATE OR REPLACE FUNCTION add_producto(
                                nombre VARCHAR(50),
                                descripcion TEXT,
                                cant_stock INTEGER,
                                precio FLOAT,
                                imagen VARCHAR(200),
                                categoria VARCHAR(100),
                                id_proveedor INTEGER,
                                tamanio_pantalla VARCHAR(10) DEFAULT NULL,
                                espacio VARCHAR(10) DEFAULT NULL,
                                memoria_ram VARCHAR(10) DEFAULT NULL,
                                consumo VARCHAR(10) DEFAULT NULL

                            ) RETURNS SETOF producto AS
                            $$
                                DECLARE
                                    resultado producto;
                                BEGIN
                                    IF categoria = 'movil' THEN
                                        INSERT INTO movil (nombre, descripcion, cant_stock, precio, imagen, categoria, id_proveedor, tamanio_pantalla, espacio, memoria_ram)
                                        VALUES (nombre, descripcion, cant_stock, precio, imagen, categoria, id_proveedor, tamanio_pantalla, espacio, memoria_ram)
                                        RETURNING * INTO resultado;

                                    ELSIF categoria = 'componente_pc' THEN
                                        INSERT INTO componente_pc (nombre, descripcion, cant_stock, precio, imagen, categoria, id_proveedor)
                                        VALUES (nombre, descripcion, cant_stock, precio, imagen, categoria, id_proveedor)
                                        RETURNING * INTO resultado;

                                    ELSIF categoria = 'equipo_hogar' THEN
                                        INSERT INTO equipo_hogar (nombre, descripcion, cant_stock, precio, imagen, categoria, id_proveedor, consumo)
                                        VALUES (nombre, descripcion, cant_stock, precio, imagen, categoria, id_proveedor, consumo)
                                        RETURNING * INTO resultado;

                                    END IF;

                                    RETURN NEXT resultado;
                                END;

                            $$
                            LANGUAGE plpgsql;
                        
                        """)
        
        cursor.execute("""
                       
                       CREATE OR REPLACE FUNCTION detalle_producto(id INTEGER) RETURNS SETOF listar_producto_detalle AS 
                       $$
                            DECLARE
                                resultado listar_producto_detalle;
                                
                            BEGIN
                                SELECT * INTO RESULTADO FROM listar_producto_detalle WHERE id_producto=id;
                                
                                IF FOUND THEN 
                                    RETURN NEXT resultado;
                                END IF;
                                
                                RETURN;
                                
                            END;
                       $$
                       LANGUAGE plpgsql;
                       
                       """)
        
        
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION actualizar_producto(
                            id INTEGER,
                            nombre VARCHAR(50),
                            descripcion TEXT,
                            cant_stock INTEGER,
                            precio FLOAT,
                            imagen VARCHAR(200),
                            categoria VARCHAR(100),
                            id_proveedor INTEGER,
                            tamanio_pantalla VARCHAR(10) DEFAULT NULL,
                            espacio VARCHAR(10) DEFAULT NULL,
                            memoria_ram VARCHAR(10) DEFAULT NULL,
                            consumo VARCHAR(10) DEFAULT NULL
                        
                        ) RETURNS SETOF listar_producto_detalle AS 
                        $$
                            DECLARE
                                resultado listar_producto_detalle;
                                nuevo_id INTEGER;
                                
                            BEGIN
                                SELECT * INTO nuevo_id FROM cambiar_categoria(id, categoria);
                                RAISE NOTICE 'valor de la variable %', nuevo_id;
                            
                                IF categoria = 'movil' THEN
                                    UPDATE movil  SET 
                                        nombre=actualizar_producto.nombre, 
                                        descripcion=actualizar_producto.descripcion, 
                                        cant_stock=actualizar_producto.cant_stock, 
                                        precio=actualizar_producto.precio, 
                                        imagen=actualizar_producto.imagen, 
                                        categoria=actualizar_producto.categoria, 
                                        id_proveedor=actualizar_producto.id_proveedor, 
                                        tamanio_pantalla=actualizar_producto.tamanio_pantalla, 
                                        espacio=actualizar_producto.espacio, 
                                        memoria_ram=actualizar_producto.memoria_ram WHERE id_producto=nuevo_id
                                    RETURNING * INTO resultado;

                                ELSIF categoria = 'componente_pc' THEN
                                    UPDATE componente_pc SET 
                                            nombre=actualizar_producto.nombre, 
                                            descripcion=actualizar_producto.descripcion, 
                                            cant_stock=actualizar_producto.cant_stock, 
                                            precio=actualizar_producto.precio, 
                                            imagen=actualizar_producto.imagen, 
                                            categoria=actualizar_producto.categoria, 
                                            id_proveedor=actualizar_producto.id_proveedor WHERE id_producto=nuevo_id
                                    RETURNING * INTO resultado;

                                ELSIF categoria = 'equipo_hogar' THEN
                                    UPDATE equipo_hogar SET 
                                            nombre=actualizar_producto.nombre, 
                                            descripcion=actualizar_producto.descripcion, 
                                            cant_stock=actualizar_producto.cant_stock, 
                                            precio=actualizar_producto.precio, 
                                            imagen=actualizar_producto.imagen, 
                                            categoria=actualizar_producto.categoria, 
                                            id_proveedor=actualizar_producto.id_proveedor,
                                            consumo=actualizar_producto.consumo WHERE id_producto=nuevo_id
                                    RETURNING * INTO resultado;

                                END IF;
                                
                                RETURN NEXT resultado;

                            END;
                        $$
                        LANGUAGE plpgsql;
                        
                       """)
        
        cursor.execute("""
                       
                       CREATE OR REPLACE FUNCTION eliminar_producto(id INTEGER) RETURNS SETOF producto AS 
                       $$
                            DECLARE
                                resultado producto;
                                
                            BEGIN
                                SELECT * INTO resultado FROM producto WHERE id_producto = id;
                                DELETE FROM producto WHERE id_producto = id;
                                
                                IF FOUND THEN 
                                    RETURN NEXT resultado;
                                END IF;
                                
                                RETURN;
                                
                            END;
                       $$
                       LANGUAGE plpgsql;
                       
                       """)
        
        cursor.execute("""
                       
                     CREATE OR REPLACE FUNCTION cambiar_categoria(id INTEGER, nueva_categoria VARCHAR(100)) RETURNS INTEGER AS 
                       $$
                            DECLARE
                                resultado listar_producto_detalle;
                                new_id INTEGER;
                                
                            BEGIN
                                SELECT * INTO resultado FROM listar_producto_detalle WHERE id_producto = id;
                                
                                IF resultado.categoria <> nueva_categoria THEN
                                    PERFORM eliminar_producto(id);
                                    SELECT id_producto INTO new_id FROM add_producto (
                                        resultado.nombre, 
                                        resultado.descripcion, 
                                        resultado.cant_stock, 
                                        resultado.precio, 
                                        resultado.imagen,
                                        nueva_categoria,  
                                        resultado.id_proveedor, 
                                        resultado.tamanio_pantalla, 
                                        resultado.espacio, 
                                        resultado.memoria_ram, 
                                        resultado.consumo);
                                    
                                    RETURN new_id;
                                END IF;
                                
                                RETURN id;
                                
                            END;
                       $$
                       LANGUAGE plpgsql;
                       
                       """)
        
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION adicionar_al_carrito(id_p INTEGER, id_c INTEGER) RETURNS SETOF cliente_producto AS
                        $$
                            DECLARE
                                resultado cliente_producto;
                                producto_del_carrito carrito;
                                el_cliente cliente;
                        
                            BEGIN
                                SELECT * INTO el_cliente FROM cliente WHERE id_usuario = id_c;
                                SELECT * INTO producto_del_carrito FROM carrito WHERE id_producto=id_p;
                                
                                IF NOT FOUND THEN
                                    INSERT INTO cliente_producto (id_producto, id_cliente) VALUES (id_p, el_cliente.id_cliente)
                                    RETURNING * INTO resultado;
    
                                    RETURN NEXT resultado;
                                END IF;
                            
                                RETURN;
    
                            END;
                        
                        $$
                        LANGUAGE plpgsql;
                       """)
        
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION obtener_carrito(id_c INTEGER) RETURNS SETOF listar_productos AS
                        $$
                            DECLARE
                                resultados listar_productos;
                                id_p INTEGER;
                                el_cliente cliente;
                        
                            BEGIN
                                SELECT * INTO el_cliente FROM cliente WHERE id_usuario = id_c;
                                
                                IF FOUND THEN
                            
                                    FOR id_p IN SELECT id_producto FROM carrito WHERE id_cliente=el_cliente.id_cliente
                                        LOOP
                                            SELECT * INTO resultados FROM listar_productos WHERE id_producto=id_p;
                                            RETURN NEXT resultadoS;
                                            
                                        END LOOP;
                                
                                END IF;
                                
                                RETURN;
    
                            END;
                        
                        $$
                        LANGUAGE plpgsql;
                       
                       """)
        
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION quitar_producto_carrito(id_p INTEGER, id_c INTEGER) RETURNS SETOF producto AS 
                        $$
                            DECLARE
                                resultado producto;
                                el_cliente cliente;
                                
                            BEGIN
                                SELECT * INTO el_cliente FROM cliente WHERE id_usuario = id_c;
                                
                                IF FOUND THEN
                            
                                    SELECT * INTO resultado FROM carrito WHERE id_producto=id_p AND id_cliente=el_cliente.id_cliente;
                                    
                                    IF FOUND THEN
                                        DELETE FROM carrito WHERE id_producto=id_p;
                                        RETURN NEXT resultado;
                                    END IF;
                                
                                END IF;
                                
                                RETURN;
                            
                            END;
                        
                        $$
                        LANGUAGE plpgsql;
                        
                       """)
        
        
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION producto_esta_en_carrito(id_p INTEGER, id_c INTEGER) RETURNS BOOLEAN AS
                        $$
                            DECLARE
                                encontrado INTEGER;
                                el_cliente cliente;
                        
                            BEGIN
                                SELECT * INTO el_cliente FROM cliente WHERE id_usuario = id_c;
                                
                                IF FOUND THEN
                                
                                    SELECT 1 INTO encontrado FROM carrito WHERE id_producto=id_p AND id_cliente=el_cliente.id_cliente;
                            
                                    IF FOUND THEN
                                        RETURN TRUE;
                                    END IF;
                                    
                                    
                                END IF;
                                
                                RETURN FALSE;
                            
                            END;

                        $$
                        LANGUAGE plpgsql;
                       """)
        
        
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION add_un_pedido(id_p INTEGER, id_c INTEGER, cant_stock INTEGER, contacto VARCHAR(255), dir_envio VARCHAR(255)) 
                        RETURNS pedido AS
                        $$
                            DECLARE
                                stock_producto INTEGER;
                                nuevo_pedido pedido;
                                max_valor INTEGER;
                                el_cliente cliente;
                        
                            BEGIN
                                SELECT * INTO el_cliente FROM cliente WHERE id_usuario = id_c;
                            
                                IF FOUND THEN                                    
                                    SELECT producto.cant_stock INTO stock_producto FROM producto WHERE id_producto = id_p;
                                    
                                    IF FOUND THEN
                                    
                                        IF cant_stock > 0 AND cant_stock <= stock_producto THEN
                                            UPDATE producto SET cant_stock=stock_producto-add_un_pedido.cant_stock WHERE id_producto=id_p;
                                            INSERT INTO pedido (id_cliente, cantidad, info_contacto, dir_envio) 
                                            VALUES (el_cliente.id_cliente, cant_stock, contacto, dir_envio)
                                            RETURNING * INTO nuevo_pedido;
                                            
                                            INSERT INTO pedido_producto(id_pedido, id_producto) VALUES (nuevo_pedido.id_pedido, id_p);
                                        
                                            RETURN nuevo_pedido;
                                        ELSE
                                            RAISE EXCEPTION 'cantidad invalida';
                                        
                                        END IF;
                                        
                                    END IF;
                                    
                                END IF;
                                
                            
                            END;

                        $$
                        LANGUAGE plpgsql;
                       """)
        
        
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION obtener_pedidos(id_c INT) RETURNS SETOF listar_pedidos AS
                        $$
                            DECLARE
                                resultados listar_pedidos;
                                el_cliente cliente;
                                
                            BEGIN
                                SELECT * INTO el_cliente FROM cliente WHERE id_usuario = id_c; 
                                SELECT * INTO resultados FROM listar_pedidos WHERE id_cliente = el_cliente.id_cliente;
                                
                                IF FOUND THEN
                                    FOR resultados IN SELECT * FROM listar_pedidos WHERE id_cliente = el_cliente.id_cliente
                                    LOOP
                                        RETURN NEXT resultadoS;
                                    END LOOP;    
                
                                END IF;
                                
                                RETURN;
                                
                            END;
                        
                        $$
                        LANGUAGE plpgsql;
                       """)
        
        cursor.execute("""
                       
                       CREATE OR REPLACE FUNCTION crear_confirmacion(id_p INTEGER, id_e INTEGER) RETURNS listar_ventas AS 
                        $$
                            DECLARE
                                resultado confirmaciones;
                                info_venta listar_ventas;
                                empleado trabajador;
                        
                            BEGIN
                                SELECT * INTO empleado FROM trabajador WHERE id_usuario = id_e;
                                
                                IF FOUND THEN
                                    INSERT INTO confirmaciones (id_pedido, id_empleado) VALUES (id_p, empleado.id_trabajador)
                                    RETURNING * INTO resultado;
                                
                                    UPDATE pedido SET estado='CONFIRMADO' WHERE id_pedido=id_p;
                                    
                                    SELECT * INTO info_venta FROM generar_venta(id_p, resultado.id_confirmacion) AS listar_ventas;
                                    
                                    RETURN info_venta;
                                    
                                END IF;
                                
                            END;
                        
                        
                        $$
                        LANGUAGE plpgsql;
                       """)
        
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION generar_venta(id_p INTEGER, id_confirmacion INTEGER) RETURNS listar_ventas AS 
                        $$
                            DECLARE
                                resultado listar_ventas;
                        
                            BEGIN
                                INSERT INTO info_ventas (id_pedido, id_confirmacion) VALUES (id_p, id_confirmacion)
                                RETURNING * INTO resultado;
                                RETURN resultado;
                             
                            END;
                        
                        
                        $$
                        LANGUAGE plpgsql;
                       
                       """)
        
        # Funcion Agregada de Ventana Clausula OVER (Optimización)
        cursor.execute("""

                        CREATE OR REPLACE FUNCTION suma_acumulativa_carrito(p_user_id INT) RETURNS TABLE(id_producto INT, precio float, suma_acumulativa float) AS 
                        $$
                       
                            BEGIN
                                RETURN QUERY 
                                SELECT listar_productos.id_producto, listar_productos.precio, SUM(listar_productos.precio) OVER(ORDER BY listar_productos.id_producto) AS suma_acumulativa
                                FROM (SELECT * FROM obtener_carrito(2)) AS listar_productos;
                            END; 
                       
                        $$
                        LANGUAGE plpgsql;
                       
                       
                        CREATE OR REPLACE FUNCTION productos_mas_vendidos() RETURNS SETOF RECORD AS 
                        $$

                            BEGIN
                                RETURN QUERY 
                                /*
                                SELECT p.id_producto, p.nombre, COUNT(*) AS cantidad
                                FROM info_ventas iv
                                JOIN pedido_producto pp ON iv.id_pedido = pp.id_pedido
                                JOIN producto p ON pp.id_producto = p.id_producto
                                GROUP BY p.id_producto, p.nombre
                                ORDER BY cantidad DESC;
                                */

                                SELECT ranking.id_producto, ranking.nombre, ranking.cantidad, RANK() OVER(ORDER BY ranking.cantidad DESC) AS rank
                                FROM (
                                    SELECT p.id_producto, p.nombre,
                                    COUNT(*) OVER (PARTITION BY p.id_producto) AS cantidad
                                    FROM info_ventas iv, pedido_producto pp, producto p
                                    WHERE iv.id_pedido = pp.id_pedido AND pp.id_producto = p.id_producto
                                ) AS ranking
                                GROUP BY ranking.nombre, ranking.id_producto, ranking.cantidad
                                ORDER BY cantidad DESC;
                            END; 

                        $$
                        LANGUAGE plpgsql;
                       
        """)

        # Funcion Agregada de Ventana Clausula WITH (Optimización)
        cursor.execute("""

                        CREATE OR REPLACE FUNCTION productos_x_categorias() RETURNS SETOF RECORD AS 
                        $$
                       
                            BEGIN
                                RETURN QUERY 
                                /*
                                SELECT categoria, COUNT(*) AS total
                                FROM producto
                                GROUP BY categoria
                                ORDER BY categoria;
                                */
                        
                                WITH nombre_temporal AS (
                                    SELECT categoria, COUNT(*) AS total
                                    FROM producto
                                    GROUP BY categoria
                                )
                                SELECT categoria, total
                                FROM nombre_temporal;
                            END; 
                       
                        $$
                        LANGUAGE plpgsql;
                       
                        CREATE OR REPLACE FUNCTION ganancia_promedio() RETURNS SETOF RECORD AS 
                        $$
                       
                            BEGIN
                                RETURN QUERY 
                                WITH ganancia_promedio AS (
                                    SELECT AVG(precio) as ganancia
                                    FROM info_ventas iv, pedido_producto pp, producto p
                                    WHERE iv.id_pedido = pp.id_pedido AND pp.id_producto = p.id_producto
                                )
                                SELECT ganancia_promedio
                                FROM ganancia_promedio;
                                
                            END; 
                       
                        $$
                        LANGUAGE plpgsql;
                       
        """)

        # Usando los indices
        cursor.execute("""

            CREATE OR REPLACE FUNCTION buscar_producto(nombre_b VARCHAR(255)) RETURNS SETOF producto AS
            $$
                BEGIN
                    RETURN QUERY
                    SELECT * FROM producto WHERE nombre LIKE '%' || nombre_b || '%';

                END;
            $$
            LANGUAGE plpgsql;
                       
            CREATE OR REPLACE FUNCTION filtrar_productos_por_categoria(categoria_f VARCHAR(255)) RETURNS SETOF producto AS
            $$
                BEGIN
                    RETURN QUERY
                    SELECT * FROM producto WHERE categoria LIKE '%' || categoria_f || '%';
                END;
            $$
            LANGUAGE plpgsql;
                       
        """)
        
        
        
        
        