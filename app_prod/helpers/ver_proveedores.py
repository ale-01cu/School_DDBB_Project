from collections import namedtuple
from django.db import connection

def get_proveedores():
    
    try: 
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM proveedor')
            proveedores = [namedtuple('proveedores', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
            return [(i.id_proveedor, i.nombre) for i in proveedores]
    except Exception as e:
        print(e)
        
    return []
        
