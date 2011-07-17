# -*- coding: utf-8 -*-
# Copyright: 2011, Grigoriy Petukhov
# Author: Grigoriy Petukhov (http://lorien.name)
# License: BSD
from datetime import datetime
import os.path

from django.test import TestCase

from feedzilla.util.parse import guess_date, parse_feed

ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(ROOT, 'test_data')

class ParserTestCase(TestCase):
    def test_guess_datetime(self):

        def create_feed(custom_language):
            class FeedMockup(object):
                "Emulates feedparser.parse() object"

                class Feed(object):
                    language = custom_language

                    def __getitem__(self, key):
                        return getattr(self, key)
                feed = Feed()
            return FeedMockup()


        date_string = 'Птн, 18 Мар 2011 02:47:00 +0300'
        feed = create_feed('ru')
        guessed = guess_date([date_string], feed)
        self.assertEqual(guessed, datetime(2011, 3, 18, 2, 47, 0))

        # set language to en, this should fail
        feed = create_feed('en')
        guessed = guess_date([date_string], feed)
        self.assertEqual(guessed, None)

        data = open(os.path.join(DATA_DIR, 'feed_with_rudate')).read()
        resp = parse_feed(source_data=data)
        # Птн, 18 Мар 2011 01:04:00 +0300
        self.assertEqual(resp['entries'][0]['created'], datetime(2011, 3, 18, 2, 47, 0))
