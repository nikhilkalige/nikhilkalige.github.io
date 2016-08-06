#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys

sys.path.append('.')
import filter_tags
from figure_alt_caption import makeExtension
from extend_image_md import ImageExtensions
from mdx_video import VideoExtension


AUTHOR = u'Nikhil K'
SITENAME = u'ShortCircuits'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Phoenix'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = 'pelican-theme'
THEME_STATIC_DIR = "static"
CSS_FILE = "index.min.css"

DEFAULT_DATE = 'fs'

AUTHOR_SAVE_AS = ''

PAGE_URL = 'projects/{slug}.html'
PAGE_SAVE_AS = 'projects/{slug}.html'
MARKUP = ('md', 'ipynb')

DIRECT_TEMPLATES = ('index', 'tags', 'projects')
JINJA_EXTENSIONS = ['jinja2.ext.loopcontrols', 'jinja2.ext.with_', 'jinja2.ext.do']
MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', makeExtension(), ImageExtensions(),
                 VideoExtension(youtube_width=800, youtube_height=450)
                ]

JINJA_FILTERS = {
    "gtag": filter_tags.group_tags
}

STATIC_PATHS = [
    'images',
    'extras/CNAME'
]

EXTRA_PATH_METADATA = {
    'extras/CNAME': {'path': 'CNAME'}
}

PLUGIN_PATHS = ['/home/lonewolf/workspace/web/pelican-plugins', './plugins']
PLUGINS = ['sitemap', 'optimize_images', 'ipynb.markup', 'series']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 1.0,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

TYPOGRIFY = True

# Ipython notebook plugin config
IPYNB_INCLUDE_CSS = False
IGNORE_FILES = ['.ipynb_checkpoints']
IPYNB_USE_META_SUMMARY = True
