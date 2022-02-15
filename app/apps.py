
from __future__ import unicode_literals
from django.apps import AppConfig



class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    
    def ready(self):
        print("at ready")
        import app.signals  #noqa
    