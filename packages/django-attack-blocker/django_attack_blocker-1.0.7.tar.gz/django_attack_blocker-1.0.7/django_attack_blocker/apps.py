from django.apps import AppConfig

class MLIPBlockerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_attack_blocker'
    verbose_name = "Django Network Attack Blocker"