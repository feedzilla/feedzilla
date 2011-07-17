# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
import random

from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

from tagging.models import Tag

from feedzilla.models import Feed, Post


register = template.Library()

@register.inclusion_tag('feedzilla/_tag_cloud.html', takes_context=True)
def feedzilla_tag_cloud(context):
    """
    Show tag cloud for specified site.
    """

    tags = Tag.objects.cloud_for_model(Post, filters={'active': True},
                                       steps=settings.FEEDZILLA_CLOUD_STEPS,
                                       min_count=settings.FEEDZILLA_CLOUD_MIN_COUNT)

    return {'tags': tags,
            }


@register.inclusion_tag('feedzilla/_donor_list.html')
def feedzilla_donor_list():
    """
    Show aggregated feed.
    """

    donors = Feed.objects.all()

    return {'donors': donors,
            }


@register.inclusion_tag('feedzilla/_feed_head.html')
def feedzilla_feed_head(feed_id, number=3):
    """
    Show last 'number' messages from feed.
    """

    try:
        feed = Feed.objects.get(pk=feed_id)
        messages = feed.posts.all().filter(active=True)[:number]
    except Feed.DoesNotExist:
        feed = None
        messages =  []

    return {'feed': feed,
            'messages': messages,
            }

@register.filter
def feedzilla_strong_spaces(text):
        return mark_safe(text.replace(u' ',u'&nbsp;'))
