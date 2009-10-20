"""
Functions for easy parsing RSS and ATOM feeds.
"""

import sha
import re
from time import mktime
from datetime import datetime
import feedparser
import logging
#from dateutil import parser

import clean

def guess_date(chunks):
    """
    Try to find date in chunks.

    Yep, shit.
    """

    #for chunk in chunks:
        #try:
            #print 'TRY', chunk
            #return parser.parse(chunk)
        #except ValueError:
            #pass

    #regexps = (
        #(re.compile(r'\d+-\d+-\d+T\d+-\d+-\d+'), '%Y-%m-%dT%H:%M:%S'),
    #)

    #for chunk in chunks:
        #print chunk
        #for rex, format in regexps:
            #match = rex.match(chunk)
            #if match:
                #return datetime.strptime(chunk, format)
            #else:
                #print 'bad rex'
    return None


def parse_modified_date(entry):
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
        guessed = guess_date(unparsed)
        if guessed:
            return guessed

    logging.error('Could not parse modified date of %s' % getattr(entry, 'link', ''))
    return None


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
        #if url:
            #source_data = urllib.urlopen(url).read()

        # Crazy hack
        #if '<rss' in source_data[:100]:
            #if '<lastBuildDate>' in source_data:
                #source_data = source_data.replace('<lastBuildDate>', '<pubDate>')
                #source_data = source_data.replace('</lastBuildDate>', '</pubDate>')
                #logging.debug('Crazy lastBuildDate hack was applyed to feed %s' % url)
                #print source_data

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
        if not created:
            continue

        tags = get_tags(entry)
        guid = sha.new(link.encode('utf-8')).hexdigest()

        entry = {'title': title, 'link': link, 'summary': summary,
                 'content': content, 'created': created,
                 'guid': guid, 'tags': tags}
        resp['entries'].append(entry)

    return resp
