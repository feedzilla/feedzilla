import random

from django import template

from feed.models import Feed, Post
from tagging.models import Tag

register = template.Library()


@register.inclusion_tag('feed/tag_cloud.html', takes_context=True)
def tag_cloud(context):
    """
    Show tag cloud for specified site.
    """

    tags = Tag.objects.cloud_for_model(Post, filters={'active': True})
    return {'tags': tags,
            }


@register.inclusion_tag('feed/donor_list.html')
def donor_list():
    """
    Show aggregated feed.
    """

    donors = Feed.objects.all()
    return {'donors': donors,
            }


@register.inclusion_tag('feed/feed_head.html')
def feed_head(feed_id, number=3):
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
