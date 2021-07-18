from os import environ
import os


SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.10,
    participation_fee=0,
    doc="",
    use_browser_bots=False,
    debug=False,
)

LANGUAGE_SESSION_KEY = '_language'

SESSION_CONFIGS = [
    {
        'name': 'dg',
        'display_name': "Session 1. Dictator Game + beliefs",
        'num_demo_participants': 3,
        'app_sequence': ['dg'],
    },

    {
        'name': 'pgg3',
        'display_name': "Public good game 3",
        'num_demo_participants': 3,
        'app_sequence': ['pggfg'],
        'nickname': True,
    },

    {
        'name': 'combined_session',
        'display_name': "PGG+DG",
        'num_demo_participants': 3,
        'app_sequence': ['dg','pggfg'],

    },

]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'token'

ROOMS = [{'name': 'hse', 'display_name': 'HSE Study'}]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'm1e8fnwh3#$v6xbng%$!jn_onduh(22hmzx$kt=$ch6+m6*lcg'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = [
    'otree',
]

MIDDLEWARE_CLASSES = ['django.middleware.locale.LocaleMiddleware', ]
USE_I18N = True


