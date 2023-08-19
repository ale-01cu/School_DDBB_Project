from collections import namedtuple
from django.shortcuts import render, redirect
from django.db import connection
from app_prod.forms.ProductosForms import ProductosForms
from django.http import JsonResponse
from app_prod.permissions import is_admin

# Create your views here.
def getProductos(request):
  productos = []
  page = int(request.GET.get('page', 0))
  cant_elementos_x_pagina = 50
  
  if page < 0: page = 0

  try:
    with connection.cursor() as cursor:
      cursor.execute(f"SELECT * FROM listar_productos LIMIT {cant_elementos_x_pagina} OFFSET {page*cant_elementos_x_pagina}")
      productos = [namedtuple('Producto', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
  
  except Exception as e:
    print(e)
    return render(request, 'error_page_cliente.html', {'error': 'Error al conectar con la base de datos'})


  with connection.cursor() as cursor:
    cursor.execute('SELECT * FROM total_productos')
    total = cursor.fetchall()[0][0]
  
  if is_admin(request.user.id):
    return render(request, 'homeEmpleado.html', {'productos': productos, 'sgte': page+1, 'prev': page-1, 'total': total, 'page': page})
  else:
    return render(request, 'homeCliente.html', {'productos': productos, 'sgte': page+1, 'prev': page-1, 'total': total, 'page': page})
  


def crearProducto(request):
  if is_admin(request.user.id):
    if request.method == 'GET':
        form = ProductosForms()
        return render(request, "productosForm.html", {'form':form})
    
    elif request.method == 'POST':
      form = ProductosForms(request.POST)
      
      if form.is_valid():
        tipo = request.POST['categoria']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        cant_stock = request.POST['cant_stock']
        precio = request.POST['precio']
        imagen = request.POST['imagen']
        id_proveedor = request.POST['id_proveedor']
        tamanio_pantalla = request.POST['tamanio_pantalla']
        espacio = request.POST['espacio']
        memoria_ram = request.POST['memoria_ram']
        consumo = request.POST['consumo']
      
        try:
          with connection.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM add_producto (
              '{nombre}', 
              '{descripcion}', 
              {cant_stock}, 
              {precio}, 
              '{imagen}', 
              '{tipo}',  
              {id_proveedor}, 
              '{tamanio_pantalla}', 
              '{espacio}', 
              '{memoria_ram}', 
              '{consumo}') AS producto 
              """)
            
            if cursor.fetchall():
              form = ProductosForms()
              return render(request, "productosForm.html", {'form':form, 'msg': f'se ha insertado el producto {nombre} correctamente'})
            
            else:
              form = ProductosForms(request.POST)
              return render(request, "productosForm.html", {'form':form, 'error': f'No se pudo insertar el elemnto'})
                
        
        except Exception as e:
          print(e)
          return render(request, "productosForm.html", {'form':form, 'error': f'Error con la base de datos.'})

        
    else:
      return render(request, 'forbidden.html')



def obtenerUnProducto(request, pk=None):  
  
  if request.method == 'GET':
    productos = []
    
    try:
      with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM detalle_producto({pk}) AS listar_producto_detalle")
        productos = [namedtuple('Producto', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
        
        cursor.execute(f"SELECT * FROM producto_esta_en_carrito({productos[0].id_producto}, {request.user.id})")
        en_carrito = cursor.fetchall()[0][0]
        
        if is_admin(request.user.id):
          return render(request, "productoDetalleEmpleado.html", {'productos': productos[0], 'en_carrito': en_carrito})
          
        else:
          return render(request, "productoDetalleCliente.html", {'productos': productos[0], 'en_carrito': en_carrito})
        
    except Exception as e:
      print(e)
      
      if is_admin(request.user.id):
        return render(request, "productoDetalleEmpleado.html", {
          'productos': productos, 
          'errpr': 'Ocurrio un error con la base de datos'
          })
      else:
        return render(request, "productoDetalleCliente.html", {
          'productos': productos, 
          'errpr': 'Ocurrio un error con la base de datos'
          })
        
  else:
    if is_admin(request.user.id):
      return render(request, 'error_page_empleado.html', {'error': 'Metodo invalido'})
       
    else:
     return render(request, 'error_page_cliente.html', {'error': 'Metodo invalido'})
        
    
    
def actualizarProducto(request, pk=None):
  
  if is_admin(request.user.id):
  
    if request.method == 'GET':
      try:
        with connection.cursor() as cursor:   
          cursor.execute(f'SELECT * FROM detalle_producto({pk}) AS listar_producto_detalle')
          
          res = cursor.fetchall()
          producto = {j[0]:i for i, j in zip(res[0], cursor.description)}
                  
          form = ProductosForms(producto)
          return render(request, "productosActualizar.html", {'form':form})
      
      except Exception as e:
        print(e)
        return render(request, 'error_page_empleado.html', {'error': 'Ocurrio un error con la base de datos'})

    
    elif request.method == 'POST':
      form = ProductosForms(request.POST)
      
      if form.is_valid():
        tipo = request.POST['categoria']
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        cant_stock = request.POST['cant_stock']
        precio = request.POST['precio']
        imagen = request.POST['imagen']
        id_proveedor = request.POST['id_proveedor']
        tamanio_pantalla = request.POST['tamanio_pantalla']
        espacio = request.POST['espacio']
        memoria_ram = request.POST['memoria_ram']
        consumo = request.POST['consumo']
      
      
        try:
          with connection.cursor() as cursor:
            cursor.execute(f"""SELECT * FROM actualizar_producto (
              {pk},
              '{nombre}', 
              '{descripcion}', 
              {cant_stock}, 
              {precio}, 
              '{imagen}', 
              '{tipo}',  
              {id_proveedor}, 
              '{tamanio_pantalla}', 
              '{espacio}', 
              '{memoria_ram}', 
              '{consumo}') AS listar_producto_detalle 
              """)
            
            prueba = cursor.fetchall()
            print("prueba", prueba)
            if prueba:
              return redirect('/home/')
            else:
              return render(request, "productosActualizar.html", {'form':form, 'error': 'No se pudo actualizar el producto'})
            
            
        except Exception as e:
          print(e)
          return render(request, "productosActualizar.html", {'form':form, 'error': 'Problemas con la base de datos'})
          
    
      return render(request, "productosActualizar.html", {'form':form, 'error': 'Formulario invalido'})
    
    else:
      return render(request, 'error_page_empleado.html', {'error': 'Metodo Invalido'})
      
  else:
    return render(request, 'forbidden.html')

      
      
def eliminarProducto(request, pk=None):
  if is_admin(request.user.id):
    try:
      with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM eliminar_producto({pk}) AS producto')

        if cursor.fetchall(): 
          return redirect('/home/')
        else:
          return render(request, 'error_page_empleado.html', {'error': 'No se puedo eliminar el elemento'})
          
      
    except Exception as e:
      print(e)
      return render(request, 'error_page_empleado.html', {'error': 'Error con la base de datos'})

    
  else:
    return render(request, 'forbidden.html') 
      
  