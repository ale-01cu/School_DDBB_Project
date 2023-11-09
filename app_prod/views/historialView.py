from django.shortcuts import render, redirect
from django.db import connection
from collections import namedtuple


def get_historial(request):
    user_id = request.user.id
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM historial_usuario WHERE id_cliente = {user_id}')
        items = [namedtuple('items', [col[0] for col in cursor.description])(*row) for row in cursor.fetchall()]
        return render(request, 'historial.html', {'items': items})