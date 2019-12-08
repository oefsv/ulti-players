from django.apps import AppConfig

class UltimateFrisbeeManagementConfig(AppConfig):
    name = 'ultimate_frisbee_management'

    def ready(self):
        from .signals import permissions