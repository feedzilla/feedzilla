import re

from django.utils.html import strip_tags

from tagging.models import Tag

filter = {}

def load_filters():
    from feed.models import FilterTag, FilterWord

    if not filter:
        tags = [x.value.upper() for x in FilterTag.objects.all()]
        words = [re.compile(ur'\b%s\b' % x.value, re.U | re.I)\
            for x in FilterWord.objects.all()]
        filter['tags'] = tags
        filter['words'] = words


def check_post(post):
    load_filters()

    for tag in Tag.objects.get_for_object(post):
        if tag.name.upper() in filter['tags']:
            return True

    title = strip_tags(post.title)
    text = strip_tags(post.content)

    return any(x.search(text) or x.search(title) for x in filter['words'])
