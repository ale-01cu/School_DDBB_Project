from django.urls import path
from .views import registro, clientesList, empleadosList, addEmpleado, login_view, logoutView

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logoutView, name='logout'),
    path('registrar/', registro, name='registrp'),
    path('clientes/', clientesList, name='verClientes'),
    path('empleados/', empleadosList, name='verEmpleados'),
    path('empleado/add/', addEmpleado, name='crearEmpleado')
    
]