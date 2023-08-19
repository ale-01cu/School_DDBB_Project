from django.db import connection
from django.http import JsonResponse

def is_admin(id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM es_empleado({id})')
            return cursor.fetchall()[0][0]
            
    except Exception as e:
        print('Error con la base de datos')
        print(e)
    
    return False