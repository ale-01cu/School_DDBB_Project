from django.apps import AppConfig
from .db.views import execute_views
from .db.functions import execute_functions
import os

class AppUserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_user_profile'
    
    
    def ready(self) -> None:
        if not os.environ.get('DJANGO_STARTUP_ONCE_USER_PROFILE'):
            os.environ['DJANGO_STARTUP_ONCE_USER_PROFILE'] = '1'
            execute_views()
            execute_functions()