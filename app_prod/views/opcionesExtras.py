from collections import namedtuple
from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
from app_prod.forms.PedidosForms import PedidoForm
from app_prod.permissions import is_admin
from app_prod.scripts.poblar import (
    llenar_productos, 
    llenarClientes, 
    llenarEmpleados,
    llenarProveedores,
    llenarPedidos
)

def opcionesExtras(request):
    if is_admin(request.user.id):
        return render(request, 'opcionesExtras.html')
        
    else:
        return render(request, 'forbidden.html')

def poblarProductos(request):
    if is_admin(request.user.id):
        llenar_productos()  
        return redirect('/home/')
    else:
        return render(request, 'forbidden.html')

def poblarClientes(request):
    if is_admin(request.user.id):
        llenarClientes()
        return redirect('/clientes/')
    else:
        return render(request, 'forbidden.html')

def poblarEmpleados(request):
    if is_admin(request.user.id):
        llenarEmpleados()
        return redirect('/empleados/')
    else:
        return render(request, 'forbidden.html')

def poblarProveedores(request):
    if is_admin(request.user.id):
        llenarProveedores()
        return redirect('/proveedores/')
    else:
        return render(request, 'forbidden.html')
    
def poblarPedidos(request):
    if is_admin(request.user.id):
        llenarPedidos()
        return redirect('/pedidos/')
    else:
        return render(request, 'forbidden.html')