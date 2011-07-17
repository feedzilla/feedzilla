# -*- coding: utf-8
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
import re

from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.core.mail import mail_admins

from common.decorators import render_to
from common.pagination import paginate
from common.forms import build_form
from tagging.models import Tag, TaggedItem

from feedzilla.models import Post, Feed
from feedzilla.forms import AddBlogForm


@cache_page(60 * 5)
@render_to('feedzilla/index.html')
def index(request):
    qs = Post.active_objects.all().select_related('feed')

    page = paginate(qs, request, settings.FEEDZILLA_PAGE_SIZE)

    return {'page': page,
            }


@cache_page(60 * 15)
@render_to('feedzilla/tag.html')
def tag(request, tag_value):
    tag = get_object_or_404(Tag, name=tag_value)
    qs = TaggedItem.objects.get_by_model(Post, tag).filter(active=True).order_by('-created')
    page = paginate(qs, request, settings.FEEDZILLA_PAGE_SIZE)

    return {'tag': tag,
            'page': page,
            }


@cache_page(60 * 15)
@render_to('feedzilla/source_list.html')
def source_list(request):

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

    page = paginate(posts, request, settings.FEEDZILLA_PAGE_SIZE)

    return {'page': page,
            'message': message,
            'query': query,
            }


@render_to('feedzilla/submit_blog.html')
def submit_blog(request):
    form = build_form(AddBlogForm, request)
    if form.is_valid():
        obj = form.save()
        success = True
        body = _('New submission for the planet: %s') % obj.url
        mail_admins(_('%s: new submission') % settings.FEEDZILLA_SITE_TITLE, body)
    else:
        success = False
    return {'form': form,
            'success': success,
            }
