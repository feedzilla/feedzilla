# -*- coding: utf-8

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
    return htmldata.tagjoin(tree)
