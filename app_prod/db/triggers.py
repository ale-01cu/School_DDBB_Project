from django.db import connection

def execute_triggers():
    print("aqui en los triggers")
    with connection.cursor() as cursor:
        cursor.execute("""

            CREATE OR REPLACE FUNCTION verificar_stock_vacio() RETURNS TRIGGER AS 
            $$
                BEGIN
                    IF (OLD.cant_stock <> 0 AND NEW.cant_stock = 0) THEN
                    SELECT * FROM productos_vacios;
                    IF FOUND THEN
                        INSERT INTO productos_vacios(id_producto) VALUES (OLD.id);
                    END IF;
                    END IF;
                    RETURN NEW;
                END;
            $$ 
            LANGUAGE plpgsql;

            CREATE TRIGGER stock_vacio
            AFTER UPDATE ON producto
            FOR EACH ROW
            EXECUTE PROCEDURE verificar_stock_vacio();
                       

            CREATE OR REPLACE FUNCTION registrar_pedido() RETURNS TRIGGER AS 
            $$
                BEGIN
                    INSERT INTO historial_usuario(id_usuario, accion) VALUES (NEW.id_usuario, 'Pedido realizado';
                    RETURN NEW;
                END;
            $$ 
            LANGUAGE plpgsql;

            CREATE OR REPLACE TRIGGER guardar_historial
            AFTER INSERT ON pedidos
            FOR EACH ROW
            EXECUTE PROCEDURE registrar_pedido();

        """)