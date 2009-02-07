import re

from django.utils.html import strip_tags

from tagging.models import Tag

filter = {}

def load_filters():
    from feed.models import FilterTag, FilterWord

    if not filter:
        tags = [x.value for x in FilterTag.objects.all()]
        words = [x.value for x in FilterWord.objects.all()]
        filter['tags'] = tags
        filter['words'] = words


def check_post(post):
    load_filters()

    for tag in Tag.objects.get_for_object(post):
        if tag.name.upper() in filter['tags'].upper():
            return True
    text = strip_tags(post.content).upper()

    for word in filter['words']:
        if re.compile(ur'\b%s\b' % word, re.U | re.I).search(text):
            return True
    return False
