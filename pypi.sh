#!/bin/sh
hg push
python setup.py register sdist upload # build_sphinx upload_sphinx
