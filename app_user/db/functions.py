from django.db import connection

def execute_functions():
    with connection.cursor() as cursor:
        
        cursor.execute("""
                        CREATE OR REPLACE FUNCTION login (name VARCHAR(255), pass VARCHAR(128))
                        RETURNS SETOF RECORD AS $$
                        DECLARE
                            usuario RECORD;
                        BEGIN   
                            SELECT * INTO usuario FROM clientes_y_trabajadores WHERE nombre = name AND password = pass;

                            IF FOUND THEN 
                                RETURN NEXT usuario;
                            END IF;
                        END;
                        $$
                        LANGUAGE plpgsql;
                        
                        """)
        
        cursor.execute("""
                        
                        CREATE OR REPLACE FUNCTION registrar_cliente (name VARCHAR(255), mail VARCHAR(255), pass VARCHAR(128), re_pass VARCHAR(128))
                        RETURNS SETOF RECORD AS $$

                            DECLARE
                                resultado RECORD;
                            BEGIN
                                IF pass <> re_pass THEN
                                    RAISE EXCEPTION 'La contraseña y la confirmación de contraseña no coinciden';
                                ELSE
                                    INSERT INTO cliente(nombre, email, password) VALUES(name, mail, pass);
                                    SELECT nombre, email, estado, id_usuario, id_cliente INTO resultado FROM cliente WHERE nombre = name;
                                    
                                    PERFORM * FROM crear_perfil(resultado.id_usuario);
                                    
                                    RETURN NEXT resultado;
                                END IF;
                            END;
                        $$
                        LANGUAGE plpgsql;
                        
                        """)
        
        cursor.execute("""
                        
                        
                        CREATE OR REPLACE FUNCTION add_trabajador(nombre VARCHAR(255), email VARCHAR(255), pass VARCHAR(128), re_pass VARCHAR(128), salario FLOAT, id_jefe INT, años_experiencia INT) 
                        RETURNS trabajador AS 
                        $$
                            DECLARE
                                trabajador_agregado trabajador;
                            BEGIN
                                IF pass <> re_pass THEN
                                    RAISE EXCEPTION 'La contraseña y la confirmación de contraseña no coinciden';
                                ELSE
                                    INSERT INTO trabajador (nombre, email, password, salario, id_jefe, años_experiencia) 
                                    VALUES (nombre, email, pass, salario, id_jefe, años_experiencia);
                                    SELECT * INTO trabajador_agregado FROM trabajador AS n WHERE n.email=add_trabajador.email;
                                    
                                    PERFORM * FROM crear_perfil(trabajador_agregado.id_usuario);
                                    
                                    RETURN trabajador_agregado;
                                END IF;
                                
                            END;
                        $$
                        LANGUAGE plpgsql;
                        
                        
                        """)
        
        cursor.execute("""
                       
                       CREATE OR REPLACE FUNCTION es_empleado(id INTEGER) RETURNS BOOLEAN AS
                       $$
                            DECLARE
                                resultado BOOLEAN;
                            BEGIN
                                SELECT EXISTS (SELECT 1 FROM trabajador WHERE id_usuario = id) INTO resultado;
                                RETURN resultado;
                            END;
                        $$
                        LANGUAGE plpgsql;
                       
                       """)
        