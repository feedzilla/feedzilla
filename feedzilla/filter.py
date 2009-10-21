"""
I do not using re.I flag in regexps because of current locale does not affect
on it. So the solution is to make both searchable text and regexp in lower case.
"""
import re
import locale

from django.utils.html import strip_tags

from tagging.models import Tag

CACHE = {}

def build_regexp(value, exact):
    value = value.lower()
    if exact:
        value = u'\b%s\b' % value
    return re.compile(ur'%s' % value, re.U)


def load_filters():
    from feedzilla.models import FilterTag, FilterWord

    if not CACHE:
        tags = []
        for obj in FilterTag.objects.all():
            tags.append(build_regexp(obj.value, obj.exact))

        words = []
        for obj in FilterWord.objects.all():
            words.append(build_regexp(obj.value, obj.exact))

        CACHE['tags'] = tags
        CACHE['words'] = words


def check_post(post):
    load_filters()

    for tag in Tag.objects.get_for_object(post):
        for filter_tag in CACHE['tags']:
            if filter_tag.search(tag.name.lower()):
                return True

    title = strip_tags(post.title).lower()
    text = strip_tags(post.content).lower()

    for filter_word in CACHE['words']:
        if filter_word.search(text) or filter_word.search(title):
            return True

    return False
