from django.apps import AppConfig
import os
from django.db import connection
from .db.functions import execute_functions
from .db.views import execute_views

class AppUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_user'
    
    def ready(self) -> None:
        if not os.environ.get('DJANGO_STARTUP_ONCE_USER'):
            os.environ['DJANGO_STARTUP_ONCE_USER'] = '1'
            execute_views()
            execute_functions()