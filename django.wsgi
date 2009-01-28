import os, sys

root = os.path.dirname(os.path.realpath(__file__))
sys.path.append(root) 

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
