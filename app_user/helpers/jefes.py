from collections import namedtuple
from django.db import connection

def get_empleados():
    
    try: 
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM listar_empleados')
            empleados = [namedtuple('empleados', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
            return [(i.id_trabajador, i.nombre) for i in empleados]
    except Exception as e:
        print(e)
        
    return []