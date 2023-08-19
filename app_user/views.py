from collections import namedtuple
from django.shortcuts import render, redirect
from django.db import connection
from app_user.models import User
from app_user.forms import Registro, RegistroAdminForm
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from app_prod.permissions import is_admin
from app_user.forms import LoginForm


def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM login('{username}', '{password}') AS (id_usuario INTEGER, nombre VARCHAR(255), password VARCHAR(128))")
                    user = cursor.fetchall()
                    
                    if user:
                        userD = authenticate(request, username=username, password=password)
                        login(request, userD)
                        
                        return redirect('home/')
                    else:
                        return render(request, 'login.html', {'form': LoginForm(), 'error': 'Usuario o contraseña incorrecto'})
                    
            except Exception as e:
                print(e)
                return render(request, 'login.html', {'form': LoginForm(), 'error': 'Ha ocurrido un error con la base de datos.'}) 
        
        else: 
            print(form.errors)
            return render(request, 'login.html', {'form': LoginForm(), 'error': 'Datos Invalidos.'}) 
          
          
   
def logoutView(request):
    logout(request)
    return redirect('/')



def registro(request):
    form = Registro()
    
    if request.method == 'GET':
        return render(request, 'registro.html', {'form': form})
    
    elif request.method == 'POST':
        form = Registro(request.POST) 
        
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            re_password = request.POST['re_password']


            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                                   
                                    SELECT * FROM registrar_cliente ('{username}', '{email}', '{password}', '{re_password}') AS
                                    (nombre VARCHAR(255), email VARCHAR(255), estado BOOLEAN, id_usuario INT, id_cliente INTEGER)
                                    
                                    """)
                    
                    if cursor.fetchall():
                        user = User.objects.create_user(username=request.POST['username'], password=password)
                        user.save()
                        
                        return redirect('/')
                    
                    else:
                        return render(request, 'registro.html', {'form': Registro(), 'error': 'No se puedo registrar al usuario.'})
                    
            except Exception as e:
                print(e)
                return render(request, 'registro.html', {'form': Registro(), 'error': 'Ha ocurrido un error con la base de datos.'})
            
        else: 
            return render(request, 'registro.html', {'form': Registro(), 'error': 'Formulario no valido.'}) 

    
    
def clientesList(request):
    if is_admin(request.user.id):
        page = int(request.GET.get('page', 0))
        cant_elementos_x_pagina = 50
        
        if page < 0: page = 0
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SELECT * FROM listar_clientes LIMIT {cant_elementos_x_pagina} OFFSET {page*cant_elementos_x_pagina}')
                clientes = [namedtuple('Clientes', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
                
                cursor.execute('SELECT * FROM listar_clientes')
                total = len(cursor.fetchall())
                return render(request, 'clientesList.html', {'clientes': clientes, 'sgte': page+1, 'prev': page-1, 'total': total, 'page': page})
            
            
        except Exception as e:
            print(e)
            return render(request, 'error_page_empleado.html', {'error': 'Ocurrio un error con la base de datos'})
        
    else:
        return render(request, 'forbidden.html')
    



def empleadosList(request):
    if is_admin(request.user.id):
        
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM listar_empleados')
                empleados = [namedtuple('Empleados', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
                return render(request, 'trabajadroesList.html', {'Empleados': empleados})    
            
        except Exception as e:
            print(e)
            return render(request, 'error_page_empleado.html', {'error': 'Ocurrio un error con la base de datos'})
        
    else:
        return render(request, 'forbidden.html')
    
    
def addEmpleado(request):
    if is_admin(request.user.id):
    
        form = RegistroAdminForm()
        
        if request.method == 'GET':
            return render(request, 'registroAdmin.html', {'form': form})
        
        elif request.method == 'POST':
            form = RegistroAdminForm(request.POST)
            
            if form.is_valid():
                username = request.POST['username']
                email = request.POST['email']
                password = request.POST['password']
                re_password = request.POST['re_password']
                salario = request.POST['salario']
                experiencia = request.POST['experiencia']
                jefe = request.POST['jefe']
                

                try:
                                    
                    with connection.cursor() as cursor:
                        cursor.execute(f"""
                                        
                                        SELECT * FROM add_trabajador('{username}', '{email}', '{password}', '{re_password}', {float(salario)}, {int(jefe)}, {int(experiencia)})
                                        AS trabajador;
                                        
                                        """)
                        if cursor.fetchall():
                            
                            user = User.objects.create_user(username=request.POST['username'], password=password, email=email, is_staff=True)
                            user.save()
                            
                            return render(request, 'registroAdmin.html', {'form': form, 'msg': 'Empleado creado correctamente.'})
                        else:
                            return render(request, 'registroAdmin.html', {'form': form, 'error': 'No se puedo registrar al empleado'})
                            
                except Exception as e: 
                    print(e)
                    return render(request, 'registroAdmin.html', {'form': form, 'error': e})
                
            else:
                return render(request, 'registroAdmin.html', {'form': form, 'error': 'Datos Invalidos.'})
                

        else:
            return render(request, 'error_page_empleado.html', {'error': 'Metodo Invalido'})
        
    else:
        return render(request, 'forbidden.html')