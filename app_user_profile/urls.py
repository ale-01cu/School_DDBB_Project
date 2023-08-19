from django.urls import path, re_path
from .views import get_perfil

urlpatterns = [
    path('perfil/', get_perfil, name='perfil-usuario')

]