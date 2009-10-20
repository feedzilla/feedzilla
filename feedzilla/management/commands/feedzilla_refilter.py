import logging
from datetime import datetime

from django.core.management.base import BaseCommand

from feedzilla.models import Post

class Command(BaseCommand):
    help = u'Refilter posts'

    def handle(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)

        for post in Post.objects.all():
            post.save()
