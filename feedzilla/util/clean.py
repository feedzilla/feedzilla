# -*- coding: utf-8
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD

import htmldata
from BeautifulSoup import BeautifulSoup

def normalize_html(data):
    """
    Make valid HTML.
    """

    return unicode(BeautifulSoup(data))


def safe_html(data):
    """
    Remove all tag attributes from html except a.href and img.src
    """
    
    data = normalize_html(data)
    tree = htmldata.tagextract(data)
    for elem in tree:
        if isinstance(elem, tuple):
            for attr in elem[1].keys():
                if 'a' == elem[0] and 'href' == attr:
                    continue
                if 'img/' == elem[0] and 'src' == attr:
                    continue
                del elem[1][attr]
    data = htmldata.tagjoin(tree)
    # Temporary hack
    # htmldata doing something shitty with html:
    # tagjoin return invalid DIV
    # Data for testing: http://py-algorithm.blogspot.com/2011/04/blog-post_3267.html
    data = normalize_html(data)
    return data
