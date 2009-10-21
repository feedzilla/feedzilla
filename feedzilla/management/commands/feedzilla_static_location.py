import logging
import os.path
from datetime import datetime

from django.core.management.base import BaseCommand

import feedzilla

class Command(BaseCommand):
    help = u'Show the location of feedzilla static files'

    def handle(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)

        src_static = os.path.join(os.path.dirname(os.path.realpath(feedzilla.__file__)), 'static')
        print src_static
