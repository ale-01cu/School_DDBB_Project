from collections import namedtuple
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth import login, authenticate, logout
from app_prod.permissions import is_admin

def get_perfil(request):
    user_id = request.user.id
    perfil = []
    
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"""
                       SELECT * FROM obtener_perfil({user_id})
                       
                       """)
            perfil = [namedtuple('Perfil', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
            
            if is_admin(user_id):
                return render(request, 'perfilEmpleado.html', {'perfil': perfil[0]})
            return render(request, 'perfil.html', {'perfil': perfil[0]})
        
        
    except Exception as e:
        print(e)
        
        if is_admin(user_id):
            return render(request, 'error_page_empleado.html', {'perfil': perfil, 'error': 'Problemas con la base de datos'})
        return render(request, 'error_page_cliente.html', {'perfil': perfil, 'error': 'Problemas con la base de datos'})
    
        
    