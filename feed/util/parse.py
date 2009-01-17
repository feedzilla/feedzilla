"""
Functions for easy parsing RSS and ATOM feeds.
"""

import sha
import re
from time import mktime
from datetime import datetime
import feedparser

import clean

def parse_time(time):
    """
    Parse datetime from string.
    """

    return datetime.fromtimestamp(mktime(time))


def parse_modified_date(entry):
    """
    Find out modified date of feed entry.
    """

    if hasattr(entry, 'modified_parsed'):
        return parse_time(entry.modified_parsed)
    if hasattr(entry, 'modified'):
        return parse_time(entry.modified)
    return datetime.now()


def get_tags(entry):
    """
    Returns a list of tag objects from an entry.
    """

    tags = set()
    if 'tags' in entry:
        for tag in entry.tags:
            if getattr(tag, 'label', None):
                term = tag.label
            else:
                term = getattr(tag, 'term', '')
            terms = term.strip().replace(',', '/').split('/')
            tags.update(x.strip() for x in terms if x.strip())
    return tags


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
        title = getattr(entry, 'title', 'untitled')
        link = getattr(entry, 'link', '')

        if hasattr(entry,'content'):
            content = entry.content[0].value
        elif hasattr(entry,'summary'):
            content = entry.summary
        elif hasattr(entry,'description'):
            content = entry.description
        else:
            continue

        summary = content[:summary_size]

        summary = clean.safe_html(summary)
        content = clean.safe_html(content)

        created = parse_modified_date(entry)
        tags = get_tags(entry)
        guid = sha.new(link.encode('utf-8')).hexdigest()

        entry = {'title': title, 'link': link, 'summary': summary,
                 'content': content, 'created': created,
                 'guid': guid, 'tags': tags}
        resp['entries'].append(entry)

    return resp
