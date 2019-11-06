from foodie.config.common import *

DEBUG = True
SECRET_KEY = 'local'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
