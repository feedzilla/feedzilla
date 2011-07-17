"""
This module provides functions to filter posts by keyword in post's content and post's tags.

I do not using re.I flag in regexps because of current locale does not affect
on it. So the solution is to make both searchable text and regexp in lower case.
"""
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
import re
import locale

from django.utils.html import strip_tags

from tagging.models import Tag

from feedzilla.models import FilterTag, FilterWord

TAGS = []
WORDS = []

def build_regexp(value, exact):
    """
    Build regexp for the tag/word filter.

    If filter `exact` attribute is one then make regexp to
    match the word, i.e., matched fragment shuld be surrounded with
    spaces or text start or text end.
    """
    value = value.lower()
    if exact:
        value = u'\b%s\b' % value
    return re.compile(ur'%s' % value, re.U | re.I)


def load_filters():
    """
    Calculate regexp objects for all filters.
    """

    for obj in FilterTag.objects.all():
        TAGS.append(build_regexp(obj.value, obj.exact))

    for obj in FilterWord.objects.all():
        WORDS.append(build_regexp(obj.value, obj.exact))


class ContentFilterProcessor(object):
    """
    This processor search for certain fragment in content and tags
    of the post and mark post as active/inactive.
    """

    def process(self, post):
        post.active = self.match_filters(post)

    def match_filters(self, post):
        for tag in Tag.objects.get_for_object(post):
            for filter_tag in TAGS:
                if filter_tag.search(tag.name.lower()):
                    return True

        title = strip_tags(post.title).lower()
        text = strip_tags(post.content).lower()

        for filter_word in WORDS:
            if filter_word.search(text) or filter_word.search(title):
                return True

        return False

load_filters()
