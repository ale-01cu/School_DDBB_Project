from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from collections import namedtuple
from app_prod.forms.ProveedorForms import ProveedorForm
from app_prod.permissions import is_admin


def listProveedor(request):
    if is_admin(request.user.id):
        proveedores = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM proveedor_telefono")
                proveedores = [namedtuple('Proveedores', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
                
            return render(request, 'proveedoresList.html', {'proveedores': proveedores})
        except Exception as e:
            print(e)
            return render(request, 'proveedoresList.html', {'proveedores': proveedores, 'error': 'Ha ocurrido un error con la base de datos.'})
        
    else: 
        return render(request, 'forbidden.html')


def crearProveedor(request):
    if is_admin(request.user.id):
        if request.method == 'GET':
            form = ProveedorForm()
            return render(request, "proveedorForm.html", {'form':form})
        
        elif request.method == 'POST':
            form = ProveedorForm(request.POST)
            
            if form.is_valid():
                nombre = request.POST['nombre']
                telefonos = request.POST.getlist('telefono')
                
                try:
                    with connection.cursor() as cursor:
                        for telefono in telefonos:
                            cursor.execute(f"SELECT * FROM insertar_proveedor('{nombre}', '{telefono}') AS proveedor")
        
                        form = ProveedorForm()
                        return render(request, "proveedorForm.html", {'form':form, 'msg': 'Proveedor agregado correctamente.'})
                
                except Exception as e:
                    print(e)
                    return render(request, "proveedorForm.html", {'form':form, 'error': 'Ocurrio un error con la base de datos.'})
            
            else:
                return render(request, "proveedorForm.html", {'form':form, 'error': 'Datos incorrectos.'})
    else:
        return render(request, 'forbidden.html')
        
    
def eliminarProveedor(request, pk=None):
    if is_admin(request.user.id):
        try:
            with connection.cursor() as cursor:
                cursor.execute(F"SELECT * FROM eliminar_proveedor({pk}) AS proveedor")
                
                if cursor.fetchall():  
                    return redirect('/proveedores/')
                else:
                    return render(request, 'error_page_empleado.html', {'error': 'No se pudo eliminar el proveedor'})


        except Exception as e:
            print(e)
            return render(request, 'error_page_empleado.html', {'error': 'Error con la base de datos'})
        
    else:
        return render(request, 'forbidden.html')
