from django.db import connection

def execute_cursors():
    with connection.cursor() as cursor:
        cursor.execute("""

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
            LANGUAGE plpgsql;

        """)
