# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
import math

from django import template
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.conf import settings

from feedzilla.models import Feed, FeedzillaTag


register = template.Library()



@register.inclusion_tag('feedzilla/_donor_list.html')
def feedzilla_donor_list(order_by=None):
    """
    Show aggregated feed.
    """

    donors = Feed.objects.all()
    if order_by:
        donors = donors.order_by(order_by)

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


@register.inclusion_tag('feedzilla/_tag_cloud.html', takes_context=True)
def feedzilla_tag_cloud(context):
    """
    Show tag cloud for specified site.
    """

    tags = FeedzillaTag.objects.annotate(count=Count('items'))
    tags = tags.filter(count__gte=settings.FEEDZILLA_CLOUD_MIN_COUNT)

    if tags:
        # normalize count values
        for tag in tags:
            tag.count = math.log(tag.count)

        min_count = min(x.count for x in tags)
        max_count = max(x.count for x in tags)
        min_weight = 1
        max_weight = int(settings.FEEDZILLA_CLOUD_STEPS)

        delta_weight = ((max_weight - min_weight) /
                        float(max(1, max_count - min_count)))

        for tag in tags:
            tag.weight = int(round(max_weight - (max_count - tag.count) * delta_weight))

    return {'tags': tags,
            }
