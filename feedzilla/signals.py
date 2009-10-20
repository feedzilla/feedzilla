from django.db.models.signals import post_save

from feedzilla.models import Post
import feedzilla.filter

def post_saved(instance, **kwargs):
    if not hasattr(instance, '_processed'):
        if instance.feed.skip_filters:
            instance.active = True
        else:
            instance.active = feedzilla.filter.check_post(instance)
        instance._processed = True
        instance.save()

def setup():
    post_save.connect(post_saved, sender=Post)
