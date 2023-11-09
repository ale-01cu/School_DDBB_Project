from faker import Faker
from django.db import connection

def llenar_productos():
    fake = Faker()
    categorias = ['componente_pc', 'movil', 'equipo_hogar']
    cont = 0

    for i in range(5000):
        nombre = fake.word()
        descripcion = fake.text()
        cant_stock = fake.random_int(min=1, max=100)
        precio = fake.pydecimal(left_digits=3, right_digits=2, positive=True)
        imagen = fake.image_url()
        id_proveedor = fake.random_int(min=1, max=50)
        #id_proveedor = fake.random_int(min=1, max=10)
        tipo = categorias[2]
        
        # if i+1 % 5000 == 0:
        #     if cont < 2: cont += 1
        #     tipo = categorias[cont]
        
        tamanio_pantalla = str(fake.random_int(min=4, max=10))
        espacio = str(fake.random_int(min=16, max=256))
        memoria_ram = str(fake.random_int(min=1, max=12))
        consumo = str(fake.random_int(min=100, max=2000))
        
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
            
from app_user.models import User 
def llenarClientes():
    fake = Faker()

    for i in range(500):
        username = fake.name()
        email = fake.email()
        password = fake.pystr(min_chars=8, max_chars=16)
        
        while User.objects.filter(username=username).exists():
            username = fake.name()
        
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT * FROM registrar_cliente ('{username}', '{email}', '{password}', '{password}') AS
                (nombre VARCHAR(255), email VARCHAR(255), estado BOOLEAN, id_usuario INT, id_cliente INTEGER)
                """)
            
        user = User.objects.create_user(username=username, password=password)
        user.save()
            
def llenarEmpleados():
    fake = Faker()

    for i in range(499):
        username = fake.name()
        email = fake.email()
        password = fake.pystr(min_chars=8, max_chars=16)
        salario = fake.random_int(min=3000, max=15000)
        experiencia = fake.random_int(min=1, max=50)
        
        while User.objects.filter(username=username).exists():
            username = fake.name()
        
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT * FROM add_trabajador('{username}', '{email}', '{password}', '{password}', {float(salario)}, {1}, {experiencia})
                AS trabajador;
                """)
            
        user = User.objects.create_user(username=username, password=password, email=email, is_staff=True)
        user.save()
            
def llenarProveedores():
    fake = Faker()

    for i in range(50):
        nombre = fake.name()
        telefono = fake.phone_number()
        
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT * FROM insertar_proveedor('{nombre}', '{telefono}') AS proveedor
                """)
            
                        
def llenarPedidos():
    fake = Faker()

    for i in range(5000):
        id_prod = fake.random_int(min=1, max=15000)
        user_id = fake.random_int(min=1, max=5000)
        cantidad = fake.random_int(min=1, max=1)
        info_contacto = fake.phone_number()
        dir_envio = fake.address()
        
        with connection.cursor() as cursor:
            cursor.execute(f"""
                SELECT * FROM add_un_pedido(
                    {id_prod}, 
                    {user_id}, 
                    {cantidad}, 
                    '{info_contacto}', 
                    '{dir_envio}') 
                """)