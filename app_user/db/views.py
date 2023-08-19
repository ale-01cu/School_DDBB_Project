from django.db import connection

def execute_views():
    with connection.cursor() as cursor:
                
        # Vistas
        cursor.execute("""
                        
                        CREATE OR REPLACE VIEW clientes_y_trabajadores AS 
                        SELECT id_usuario, nombre, password FROM usuario
                        
                        """)
        
        cursor.execute("""
                        
                        CREATE OR REPLACE VIEW listar_clientes AS
                        SELECT nombre, email, estado, fecha_creado, id_cliente FROM cliente;
                        
                        """)
        
        cursor.execute("""
                        
                        
                        CREATE OR REPLACE VIEW listar_empleados AS 
                        SELECT id_trabajador, nombre, email, fecha_creado, estado, salario, años_experiencia, id_jefe FROM trabajador
                        
                        
                        """)