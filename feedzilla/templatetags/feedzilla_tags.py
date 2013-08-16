# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD

from django import template
from django.utils.safestring import mark_safe

from feedzilla.models import Feed


register = template.Library()



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
