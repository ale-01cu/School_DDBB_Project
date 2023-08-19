from collections import namedtuple
from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from app_prod.forms.PedidosForms import PedidoForm
from app_prod.permissions import is_admin

def get_pedidos(request):
    pedidos = []
    user = request.user
    user_id = user.id
    
    if is_admin(user_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM listar_pedidos')
                pedidos = [namedtuple('Pedido', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
                
                return render(request, 'pedidosListEmpleados.html', {
                    'pedidos': pedidos, 
                    'is_admin': is_admin(user_id)
                })
                
            
        except Exception as e:
            print(e)
            return render(request, 'error_page_empleado.html', {'error': 'Ha ocurrido un error al conectar con la base de datos'})
            
    
    else:
        if user.id:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f'SELECT * FROM obtener_pedidos({user_id})')
                    pedidos = [namedtuple('Pedido', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
                    return render(request, 'pedidosList.html', {'pedidos': pedidos})
                
            except Exception as e:
                print(e)
                return render(request, 'error_page_cliente.html', {'error': 'Ha ocurrido un error al hacer la consulta a la base de datos'})
        else:
            return JsonResponse({'error': 'Logeese por favor'})


def addPedido(request, id_prod=None):
    user_id = request.user.id
    
    if request.method == 'GET':
        form = PedidoForm()
        return render(request, 'pedidosForm.html', {'form': form})
    
    elif request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
        info_contacto = request.POST['info_contacto']
        dir_envio = request.POST['dir_envio']
        
        if cantidad == 0:
            return render(request, 'pedidosForm.html', {'form': form, 'error': 'Pida una cantidad por favor'})
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM add_un_pedido({id_prod}, {user_id}, {cantidad}, '{info_contacto}', '{dir_envio}') ")
                nuevo_pedido = cursor.fetchall()
                            
                if nuevo_pedido:
                    form = PedidoForm()
                    return render(request, 'pedidosForm.html', {'form': form, 'msg': 'Se inserto el pedido correctamente'})
                else:
                    form = PedidoForm(request.POST)
                    return render(request, 'pedidosForm.html', {'form': form, 'msg': 'No se pudo crear el pedido.'})
                        
        except Exception as e:
            print(e)
            return render(request, 'error_page_cliente.html', {'error': 'Ocurrio un error al insertar el pedido a la base de datos.'})
                
            
            