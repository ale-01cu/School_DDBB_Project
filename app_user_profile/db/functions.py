from django.db import connection

def execute_functions():
    with connection.cursor() as cursor:
        cursor.execute("""
                       
                       CREATE OR REPLACE FUNCTION crear_perfil (id_usuario INT)
                        RETURNS VOID AS $$
                        DECLARE
                            perfil perfil_usuario;
                        
                        BEGIN
                            SELECT * INTO perfil FROM perfil_usuario pu WHERE pu.id_perfil = crear_perfil.id_usuario;

                            IF NOT FOUND THEN
                                INSERT INTO perfil_usuario (id_perfil) VALUES (id_usuario);
                                
                            END IF;
                            
                        END;
                        $$
                        LANGUAGE plpgsql;
                        
                        
                        CREATE OR REPLACE FUNCTION obtener_perfil (id_usuario INT)
                        RETURNS listar_perfiles AS $$
                        DECLARE
                            perfil listar_perfiles;
                        BEGIN   
                            SELECT * INTO perfil FROM listar_perfiles p WHERE p.id_perfil = obtener_perfil.id_usuario;
                            
                            IF FOUND THEN
                                RETURN perfil;
                            END IF;
                            
                            RAISE EXCEPTION 'No se encontro el perfil de usuario';
                        END;
                        $$
                        LANGUAGE plpgsql;
                    
                       
                       """)
        