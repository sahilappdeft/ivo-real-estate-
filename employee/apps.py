from django.apps import AppConfig


class OfficeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employee'
    
    def ready(self):
        import employee.signals  # Import signals module