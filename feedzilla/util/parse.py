"""
This module provides `parse_feed` function which
uses `feedparser` power to parse RSS/Atom feeds.
`feedparser` return parsed feed as it is. If you need
post's content then you have to check `content`, `summary`,
`description` attributes of the feed entry. The same is true
for updated time and some other things.
`parse_feed` tries to normalize these thinkgs. You'll always
get content in `content` attribute and updated time in `created` attribute.
Also `parse_feed` tries to parse non-English variants of updated time and
extract tags.
"""
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
import locale
import sha
import re
from time import mktime
from datetime import datetime
import feedparser
import logging

import clean

log = logging.getLogger('feedzilla.util.parse')

def guess_date(dates, feed):
    """
    Try to parse date in non-standart format.
    """

    parsed = None
    oldlocale = locale.getlocale()

    for date_string in dates:
        tz_offset = re.compile(r'\s+\+(\d{2})(\d{2})$')
        match = tz_offset.search(date_string)
        # TODO: implement processing TZ offset
        # and normalizing the date to the project's TZ
        if match:
            date_string = tz_offset.sub('', date_string)
        else:
            pass

        lang = feed.feed.language[:2]
        # strptime fails on unicode
        if isinstance(date_string, unicode):
            date_string = date_string.encode('utf-8')

        if not lang.startswith('en'):
            try:
                locale_name = str('%s_%s.UTF-8' % (lang.lower(), lang.upper()))
                locale.setlocale(locale.LC_ALL, locale_name)
            except locale.Error:
                pass
            # try localized RFC 822 format
            try:
                parsed = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S')
            except ValueError:
                pass
            else:
                break
    locale.setlocale(locale.LC_ALL, oldlocale)
    return parsed


def parse_modified_date(entry, feed):
    """
    Find out modified date of feed entry.
    """

    parsed = []
    unparsed = []

    keys = ['published', 'created', 'updated', 'modified']
    for key in keys:
        value = getattr(entry, '%s_parsed' % key, None)
        if value:
            parsed.append(value)
        value = getattr(entry, key, None)
        if value:
            unparsed.append(value)

    if parsed:
        time_tuple = parsed[0]
        return datetime.fromtimestamp(mktime(time_tuple))

    if unparsed:
        guessed = guess_date(unparsed, feed)
        if guessed:
            return guessed

    return None


def get_tags(entry):
    "Return a list of tag objects of the entry"

    tags = set()
    if 'tags' in entry:
        for tag in entry.tags:
            if getattr(tag, 'label', None):
                term = tag.label
            else:
                term = getattr(tag, 'term', '')
            terms = term.strip().replace(',', '/').split('/')
            tags.update(x.strip() for x in terms if x.strip())

    # Ok. Now let's delete duplicates in different case.
    tag_map = dict((x.lower(), x) for x in tags)
    return tag_map.values()


def parse_feed(url=None, source_data=None, summary_size=1000, etag=None):
    """
    Parse feed from url or source data.

    Returns dict with feed, entries and success flag
    """

    if not url and not source_data:
        raise Exception('parse_feed requires url or source_data argument')

    resp = {'feed': None, 'success': False, 'entries': [], 'error': None}

    try:
        resp['feed'] = feedparser.parse(url and url or source_data)
    except Exception, ex:
        resp['error'] = ex
        log.error('Feed parsing failed', exc_info=ex)
        return resp
    else:
        resp['success'] = True

    # need testing
    #if resp['success'] and url:
        #if hasattr(resp['feed'], 'status'):
            #if etag and 304 == resp['feed'].status:
                #logging.debug('Feed has not been changed since last check')
                #return resp
            ## wtf that doing?
            #if 400 < resp['feed'].status:
                #return resp

    if not resp['feed'].get('etag'):
        resp['feed'].etag = ''
        resp['feed'].last_checked = datetime.now()

    for entry in resp['feed'].entries:
        try:
            link = getattr(entry, 'link', '')

            # Do not process entries without title
            if not hasattr(entry, 'title'):
                log.error('Post %s does not has a title' % link)
                continue

            title = entry.title

            if hasattr(entry,'content'):
                content = entry.content[0].value
            elif hasattr(entry,'summary'):
                content = entry.summary
            elif hasattr(entry,'description'):
                content = entry.description
            else:
                # Use title as fallback variant for the post's content
                content = title

            summary = content[:summary_size]

            summary = clean.safe_html(summary)
            content = clean.safe_html(content)

            created = parse_modified_date(entry, resp['feed'])
            if not created:
                log.error('Post %s does not has modified date' % link)
                continue

            tags = get_tags(entry)
            guid = sha.new(link.encode('utf-8')).hexdigest()

            entry = {
                'title': title,
                'link': link,
                'summary': summary,
                'content': content,
                'created': created,
                'guid': guid,
                'tags': tags,
            }
            resp['entries'].append(entry)
        except Exception, ex:
            logging.error(ex)

    return resp
