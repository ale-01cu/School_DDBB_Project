from collections import namedtuple
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from app_prod.permissions import is_admin


def crearConfirmacion(request, id_pedido=None):
    user_id = request.user.id
    
    if is_admin(user_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM crear_confirmacion({id_pedido}, {user_id}) AS confirmaciones')

                if cursor.fetchall(): return redirect('/pedidos/')                
                else:  return render(request, 'error_page_empleado.html', {'error': 'Ha ocurrido un error al ejecutar la consulta.'})
                
        except Exception as e:
            print(e)
            return render(request, 'error_page_empleado.html', {'error': 'Ha ocurrido un error al ejecutar la consulta.'})
        
    else: 
        return JsonResponse({'error': 'Logeese por favor'})
    
    
    
# def quitarConfirmacion(request, id_pedido=None):
#     user_id = request.user.id
    
#     if is_admin(user_id):
#         try:
#             with connection.cursor() as cursor:
#                 cursor.execute(f'DELETE FROM info_ventas WHERE id_pedido={id_pedido}')
#                 cursor.execute(f'DELETE FROM confirmaciones WHERE id_pedido={id_pedido} AND id_empleado={user_id}')
#                 if cursor.rowcount > 0:
#                     cursor.execute(f"UPDATE pedido SET estado='PENDIENTE' WHERE id_pedido={id_pedido}")
#                     return JsonResponse({'msg': 'Se ha quitado la confirmacion correctamente'})
#                 else:
#                     return JsonResponse({"error": "Ha ocurrido un error al ejecutar la consulta."})
                
                
#         except Exception as e:
#             print(e)
#             return JsonResponse({'error': 'Ha ocurrido un error al conectar con la base de datos'})
        
#     else: 
#         return JsonResponse({'error': 'Logeese por favor'})