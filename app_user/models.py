from django.db import models
from django.contrib.auth.models import UserManager, User
from django.db import connection
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser

class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        return super().create_user(username, email, password, **extra_fields)     
    
    def create_superuser(self, username, email, password, **extra_fields):
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""
                            SELECT * FROM add_trabajador('{username}', '{email}', '{password}', '{password}', 5000, null, 10)
                                AS trabajador;
                            """)
        except Exception as e:
            print(e)    
        
        return super().create_superuser(username, email, password, **extra_fields)
    
class User(AbstractUser):
    # campos del modelo
    objects = CustomUserManager()