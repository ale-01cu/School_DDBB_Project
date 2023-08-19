from django.db import connection

def execute_views():
    with connection.cursor() as cursor:
                
        # Vistas
        cursor.execute("""
                        
                        CREATE OR REPLACE VIEW listar_perfiles AS 
                        SELECT 
                        p.id_perfil, 
                        u.nombre, 
                        u.email ,
                        u.fecha_creado ,
                        p.ci
                        FROM perfil_usuario p 
                        LEFT JOIN usuario u ON u.id_usuario = p.id_perfil
                        
                        """)