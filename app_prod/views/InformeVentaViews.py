from collections import namedtuple
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

def listInfoVentas(request):
    user_id = request.user.id
    
    if user_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM listar_ventas')
                info_ventas = [namedtuple('ventas', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
                return render(request, 'InfoVentasList.html', {'ventas': info_ventas})
                
        except Exception as e:
            print(e)
            return render(request, 'error_page_empleado.html', {'error': 'Ha ocurrido un error al conectar con la base de datos'})
        
    else: 
        return JsonResponse({'error': 'Logeese por favor'})