from django.apps import AppConfig
from django.conf import settings


class PGGFGConfig(AppConfig):
    name = 'pggfg'


    def ready(self):
        """Just injecting i18n and otree tags so they are not fucking loaded in each page template"""
        t = settings.TEMPLATES[0]
        t['OPTIONS']['builtins'] = [
            'otree.templatetags.otree',
            'django.templatetags.i18n'
        ]
