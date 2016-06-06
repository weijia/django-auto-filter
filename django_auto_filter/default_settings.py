# import os
#
INSTALLED_APPS += (
    'django.contrib.staticfiles',
    'bootstrapform',
    'django_tables2',
    'django_tables2_reports',
    'webmanager',
    'django_auto_filter',
)
#
# STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
)

# Not working
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     )
# }

MIDDLEWARE_CLASSES += (
    'reversion.middleware.RevisionMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
            ],
        },
    },
]

# STATIC_ROOT = os.path.join('D:\\work\\codes\\new_base\\', 'static')
