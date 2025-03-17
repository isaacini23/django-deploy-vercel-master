from django.apps import AppConfig


class CustomApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_api'
