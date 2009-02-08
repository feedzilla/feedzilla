# -*- coding: utf-8
import re

from django.core.urlresolvers import reverse
from django.conf import settings

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


@render_to('feed/post.html')
def post(request, post_id):
    post = Post.active_objects.get(pk=post_id)
    #ft_query = fulltext_search_query(' '.join(re.split(ur'\s+', post.title)[:5]))

    return {'verbose': True,
            'post': post,
            } 


@render_to('feed/feed.html')
def feed(request, feed_id):
    feed = Feed.objects.get(pk=feed_id)
    last_posts = feed.posts.all().filter(active=True)[:10]

    return {'feed': feed,
            'last_posts': last_posts,
            }


@render_to('feed/tag.html')
def tag(request, tag_value):
    tag = Tag.objects.get(name=tag_value)
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
