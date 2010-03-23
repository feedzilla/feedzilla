# -*- coding: utf-8
import re

from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page

from common.decorators import render_to
from common.pagination import paginate
from common.forms import build_form
from tagging.models import Tag, TaggedItem

from feedzilla.models import Post, Feed
from feedzilla import settings as app_settings
from feedzilla.forms import AddBlogForm


@cache_page
@render_to('feedzilla/index.html')
def index(request):
    qs = Post.active_objects.all().select_related('feed')

    page = paginate(qs, request, app_settings.PAGE_SIZE)

    return {'page': page,
            }


@cache_page
@render_to('feedzilla/tag.html')
def tag(request, tag_value):
    tag = get_object_or_404(Tag, name=tag_value)
    qs = TaggedItem.objects.get_by_model(Post, tag).filter(active=True).order_by('-created')
    page = paginate(qs, request, app_settings.PAGE_SIZE)

    return {'tag': tag,
            'page': page,
            }


@cache_page
@render_to('feedzilla/sources.html')
def sources(request):

    feeds = Feed.objects.all()

    cursor = connection.cursor()
    cursor.execute("""
        SELECT f.id, COUNT(*)
        FROM feedzilla_feed f
        JOIN feedzilla_post p
            ON p.feed_id = f.id AND p.active
        GROUP BY f.id
    """)

    count_map = dict(cursor.fetchall())
    for feed in feeds:
        feed.post_count = count_map.get(feed.pk, 0)


    return {'feed': feeds,
            }


@render_to('feedzilla/search.html')
def search(request):
    query = request.GET.get('query', '')
    min_limit = 2
    if len(query) < min_limit:
        posts = []
        message = _('Your query is shorter than %d characters') % min_limit
    else:
        posts = Post.active_objects.filter(content__icontains=query)
        message = ''

    page = paginate(posts, request, app_settings.PAGE_SIZE)

    return {'page': page,
            'message': message,
            'query': query,
            }


@cache_page
@render_to('feedzilla/submit_blog.html')
def submit_blog(request):
    form = build_form(AddBlogForm, request)
    success = None
    if form.is_valid():
        form.save()
        success = _('Thanks, your submission has been accepted and will be '
                    'reviewed by admin')
    return {'form': form,
            'success': success,
            }
