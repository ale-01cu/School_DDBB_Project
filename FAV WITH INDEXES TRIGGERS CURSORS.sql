# Funcion Agregada de Ventana Clausula OVER (Optimización)
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



# Funcion Agregada de Ventana Clausula WITH (Optimización)
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

		WITH productos_categorias AS (
			SELECT categoria, COUNT(*) AS total
			FROM producto
			GROUP BY categoria
		)
		SELECT categoria, total
		FROM productos_categorias;
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



# indices
CREATE INDEX idx_nombre ON producto (nombre);

CREATE OR REPLACE FUNCTION buscar_producto(nombre_b VARCHAR(255)) RETURNS SETOF producto AS
$$
	BEGIN
		RETURN QUERY
		SELECT * FROM producto WHERE nombre LIKE '%' || nombre_b || '%';

	END;
$$
LANGUAGE plpgsql;
			
CREATE INDEX idx_categoria ON producto (categoria);

CREATE OR REPLACE FUNCTION filtrar_productos_por_categoria(categoria_f VARCHAR(255)) RETURNS SETOF producto AS
$$
	BEGIN
		RETURN QUERY
		SELECT * FROM producto WHERE categoria LIKE '%' || categoria_f || '%';
	END;
$$
LANGUAGE plpgsql;

				

# Triggers
CREATE OR REPLACE FUNCTION verificar_stock_vacio() RETURNS TRIGGER AS  
$$ 
	DECLARE  
		prod RECORD; 
	BEGIN 
		RAISE NOTICE 'Hola, mundo!'; 
		IF (OLD.cant_stock <> 0 AND NEW.cant_stock = 0) THEN 
			SELECT * INTO prod FROM productos_vacios WHERE id_producto = OLD.id_producto; 
			IF NOT FOUND THEN 
				INSERT INTO productos_vacios(id_producto) VALUES (OLD.id_producto);
			END IF; 
		END IF; 
		RETURN NEW; 
	END; 
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER stock_vacio 
AFTER UPDATE ON producto 
FOR EACH ROW 
EXECUTE PROCEDURE verificar_stock_vacio();



CREATE OR REPLACE FUNCTION registrar_pedido() RETURNS TRIGGER AS $$
	BEGIN
		INSERT INTO historial_usuario(id_cliente, accion) VALUES (NEW.id_cliente, 'Pedido realizado');
		RETURN NEW;
	END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER guardar_historial
AFTER INSERT ON pedido
FOR EACH ROW
EXECUTE PROCEDURE registrar_pedido();


# Cursores
CREATE OR REPLACE FUNCTION aumentar_precios(cantidad INT) RETURNS VOID AS
$$																

	DECLARE 
		producto_rec RECORD;
		cur CURSOR FOR SELECT * FROM producto;		

	BEGIN
		OPEN cur;
		LOOP
			FETCH NEXT FROM cur INTO producto_rec;
			EXIT WHEN NOT FOUND;

			-- Actualiza la fila en la tabla 'producto'
			UPDATE producto
			SET precio = producto_rec.precio + cantidad
			WHERE id_producto = producto_rec.id_producto;														

		END LOOP;
		CLOSE cur;													
	END;														
$$ 
LANGUAGE plpgsql;
			

CREATE OR REPLACE FUNCTION disminuir_precios(cantidad INT) RETURNS VOID AS
$$																

	DECLARE 
		producto_rec RECORD;
		cur CURSOR FOR SELECT * FROM producto;		

	BEGIN
		OPEN cur;
		LOOP
			FETCH NEXT FROM cur INTO producto_rec;
			EXIT WHEN NOT FOUND;

			-- Actualiza la fila en la tabla 'producto'
			UPDATE producto
			SET precio = producto_rec.precio - cantidad
			WHERE id_producto = producto_rec.id_producto;														

		END LOOP;
		CLOSE cur;													
	END;														
$$ 
LANGUAGE plpgsql



CREATE USER emiliano WITH ENCRYPTED PASSWORD '12345678';
CREATE USER anita WITH ENCRYPTED PASSWORD '12345678';
CREATE USER frank WITH ENCRYPTED PASSWORD '12345678';


GRANT SELECT, UPDATE, DELETE, CREATE ON producto TO emiliano;																																													
GRANT SELECT, UPDATE, DELETE, CREATE ON proveedor TO frank;																													
GRANT SELECT ON info_ventas TO anita;