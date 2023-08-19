from django.db import connection

def ganancia():
    with connection.cursor() as cursor:
        cursor.execute("""
                       
                        CREATE OR REPLACE FUNCTION ganancia(id_pedido INTEGER) RETURNS FLOAT AS 
                        $$
                            DECLARE
                                ganancia FLOAT;
                                el_producto INTEGER;
                                la_cantidad INTEGER;
                                el_precio FLOAT;
                        
                            BEGIN
                                SELECT id_producto, cantidad INTO el_producto, la_cantidad FROM listar_pedidos lp WHERE lp.id_pedido=ganancia.id_pedido;
                                
                                IF FOUND THEN
                                    SELECT precio INTO el_precio FROM producto WHERE id_producto=el_producto;
                                    ganancia = el_precio*la_cantidad;
                                    
                                    RETURN ganancia;
                                END IF;
                                
                                RAISE NOTICE  'Pedido no encontrado';

                            END;
                        $$
                        LANGUAGE plpgsql;
                       
                       """)