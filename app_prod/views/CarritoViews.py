from collections import namedtuple
from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from app_prod.permissions import is_admin

def addCarrito(request, id_prod=None):
    user_id = request.user.id

    if user_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM adicionar_al_carrito({id_prod}, {user_id})')
                return redirect(f'/obtener/{id_prod}/')
            
        except Exception as e:
            print(e)
            return render(
                request, 
                'error_page_cliente.html', 
                {'error': 'Ha ocurrido un error al conectar con la base de datos'}
            )
                    
    else:
        return JsonResponse({'error': 'Logeese por favor'})
    


def getCarrito(request):
    user_id = request.user.id
    
    if user_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM obtener_carrito({user_id}) AS listar_productos')
                productos = [namedtuple('Producto', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]  

                cursor.execute(f'SELECT * FROM suma_acumulativa_carrito({user_id})')
                suma = [namedtuple('suma_acumulada', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]  
                print(suma)
                return render(
                    request, 
                    'carritoListProductos.html', 
                    {
                        'productos': productos,
                        'suma_acumulativa': suma
                    }
                )
            
        except Exception as e:
            print(e)
            return render(
                request, 
                'error_page_cliente.html', 
                {'error': 'Ha ocurrido un error al conectar con la base de datos'}
            )
        
    else:
        return JsonResponse({'error': 'Logeese por favor'})

            
def eliminarDelCarrito(request, id_prod=None):
    user_id = request.user.id
    
    if user_id:
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM quitar_producto_carrito({id_prod}, {user_id})')
                if cursor.fetchall():
                    return redirect('/carrito/')
                else:
                    return redirect('/carrito/')
                
            
        except Exception as e:
            print(e)
            return render(
                request, 
                'error_page_cliente.html', 
                {'error': 'Ha ocurrido un error al conectar con la base de datos'}
            )

    else:
        return JsonResponse({'error': 'Logeese por favor'})