from django.apps import AppConfig
import os
from app_prod.db.views import execute_views
from app_prod.db.functions import execute_functions
from app_prod.db.function_ganancia import ganancia
from app_prod.db.indexes import execute_indexes
from app_prod.db.triggers import execute_triggers
from app_prod.db.cursors import execute_cursors

class AppProdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_prod'
    ready_executed = False
    
    def ready(self) -> None:
        if not os.environ.get('DJANGO_STARTUP_ONCE_PROD'):
            os.environ['DJANGO_STARTUP_ONCE_PROD'] = '1'
            ganancia()
            execute_views()
            execute_functions()
            # execute_indexes()
            # execute_triggers()
            execute_cursors()