from foodie.config.common import *

import django_heroku
django_heroku.settings(locals())

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
