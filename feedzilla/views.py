# -*- coding: utf-8
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins

from common.pagination import paginate

from feedzilla.models import Post, Feed, FeedzillaTag
from feedzilla.forms import AddBlogForm


def index(request):
    qs = Post.active_objects.all().select_related('feed')
    page = paginate(qs, request, settings.FEEDZILLA_PAGE_SIZE)
    context = {'page': page,
            }
    return render(request, 'feedzilla/index.html', context)


def tag(request, tag_value):
    try:
        tag = FeedzillaTag.objects.get(slug=tag_value)
    except FeedzillaTag.DoesNotExist:
        tag = get_object_or_404(FeedzillaTag, name=tag_value)
        return redirect('feedzilla_tag', tag.slug, permanent=True)

    qs = Post.objects.filter(tags=tag, active=True).order_by('-created')
    page = paginate(qs, request, settings.FEEDZILLA_PAGE_SIZE)

    context = {
        'tag': tag.name,
        'page': page
    }

    return render(request, 'feedzilla/tag.html', context) 


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

    context = {'feed': feeds,
            }
    return render(request, 'feedzilla/source_list.html', context)


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

    context = {'page': page,
            'message': message,
            'query': query,
            }
    return render(request, 'feedzilla/search.html', context)


def submit_blog(request):
    form = AddBlogForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        success = True
        body = _('New submission for the planet: %s') % obj.url
        mail_admins(_('%s: new submission') % settings.FEEDZILLA_SITE_TITLE, body)
    else:
        success = False
    context = {'form': form,
            'success': success,
            }
    return render(request, 'feedzilla/submit_blog.html', context)


def cloud_page(request):
    context = {}
    return render(request, 'feedzilla/cloud_page.html', context)
