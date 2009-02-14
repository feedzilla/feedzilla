# -*- coding: utf-8
import re

from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404

from common.decorators import render_to, paged
from tagging.models import Tag, TaggedItem
from feed.models import Post, Feed
from common.util import paginate


@render_to('index.html')
def index(request):
    qs = Post.active_objects.all().select_related('feed')
    page, paginator = paginate(qs, request, settings.FEEDZILLA_PAGE_SIZE)

    return {'page': page,
            'paginator': paginator,
            }


@render_to('feed/tag.html')
def tag(request, tag_value):
    tag = get_object_or_404(Tag, name=tag_value)
    qs = TaggedItem.objects.get_by_model(Post, tag).filter(active=True).order_by('-created')
    page, paginator = paginate(qs, request, settings.FEEDZILLA_PAGE_SIZE)

    return {'tag': tag,
            'page': page,
            'paginator': paginator
            }


@render_to('feed/sources.html')
def sources(request):
    return {'feed': Feed.objects.all(),
            }


@render_to('feed/search.html')
def search(request):
    query = request.GET.get('query', '') 
    min_limit = 2
    if len(query) < min_limit:
        posts = []
        message = u'Ваш запрос короче %d символов' % min_limit
    else:
        posts = Post.active_objects.filter(content__icontains=query)
        message = ''

    page, paginator = paginate(posts, request, settings.FEEDZILLA_PAGE_SIZE)
    return {'page': page,
            'paginator': paginator,
            'message': message,
            'query': query,
            }
