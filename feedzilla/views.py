# -*- coding: utf-8
import re

from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404

from common.decorators import render_to, paged
from common.util import paginate
from tagging.models import Tag, TaggedItem

from feedzilla.models import Post, Feed
from feedzilla import settings as app_settings


@render_to('index.html')
def index(request):
    qs = Post.active_objects.all().select_related('feed')
    page, paginator = paginate(qs, request, app_settings.PAGE_SIZE)

    return {'page': page,
            'paginator': paginator,
            }


@render_to('feedzilla/tag.html')
def tag(request, tag_value):
    tag = get_object_or_404(Tag, name=tag_value)
    qs = TaggedItem.objects.get_by_model(Post, tag).filter(active=True).order_by('-created')
    page, paginator = paginate(qs, request, app_settings.PAGE_SIZE)

    return {'tag': tag,
            'page': page,
            'paginator': paginator
            }


@render_to('feedzilla/sources.html')
def sources(request):

    return {'feed': Feed.objects.all(),
            }


@render_to('feedzilla/search.html')
def search(request):
    query = request.GET.get('query', '') 
    min_limit = 2
    if len(query) < min_limit:
        posts = []
        message = u'Ваш запрос короче %d символов' % min_limit
    else:
        posts = Post.active_objects.filter(content__icontains=query)
        message = ''

    page, paginator = paginate(posts, request, app_settings.PAGE_SIZE)

    return {'page': page,
            'paginator': paginator,
            'message': message,
            'query': query,
            }
