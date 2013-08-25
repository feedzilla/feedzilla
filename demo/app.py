import os
import sys
import os.path
import site

root = os.path.dirname(__file__)
if not root in sys.path[:1]:
    sys.path.insert(0, root)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#from django.core.handlers.wsgi import WSGIHandler
#application = WSGIHandler()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
