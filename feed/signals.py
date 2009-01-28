from django.db.models.signals import post_save

from feed.models import Post
import feed.filter

def post_saved(instance, **kwargs):
    if not hasattr(instance, '_processed'):
        instance.active = feed.filter.check_post(instance)
        instance._processed = True
        instance.save()

def setup():
    post_save.connect(post_saved, sender=Post)
