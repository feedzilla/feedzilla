============================
Feedzilla Django Application
============================

Changelog
=========

0.20::
----

* lxml instead BeautifulSoup
* New dependencies: lxml, grab
* Templates for ATOM/RSS feed moved to templates/feedzilla/feed directory


About feedzilla
===============

This is Django application that adds to your site ability to aggregate
ATOM/RSS feeds and display them in single stream. In other words you can
use feedzilla to build planet site.

Project page: http://bitbucket.org/lorien/feedzilla

Installation
============

* Use ``pip`` or ``easy_install`` to install *feedzilla* package.
* Install dependencies (see below).
* Add feedzilla to INSTALLED_APPS.
* Run ``manage.py syncdb`` or ``manage.py syncdb --migrate`` if you use South.
* Include ``url('', include('feedzilla.urls'))`` in url config.
* Setup Site instance via Django admin interface.
* Setup feedzilla settings via settings.py. See available settings below.
  You have to import default settings with ``from feedzilla.settings import *``
  line.
* Setup static files. You should copy or symlink ``static/feedzilla`` directory
  contents from feedzilla installation directory to your ``%MEDIA_ROOT%``.
* Play with templates. Probably you'll want override some of default templates.

Dependencies
============

* django-common
* django-tagging
* feedparser
* lxml
* grab

Settings
========

* ``FEEDZILLA_PAGE_SIZE`` - number of items per page
* ``FEEDZILLA_SUMMARY_SIZE``
* ``FEEDZILLA_SITE_TITLE`` - used in feed generation
* ``FEEDZILLA_SITE_DESCRIPTION`` - used in feed generation

For actual list of settings look into ``feedzilla/settings.py``
