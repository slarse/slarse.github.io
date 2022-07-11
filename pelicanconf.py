#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Simon Larsén"
SITENAME = "Programming for fun and profit"
SITEURL = ""

SITESUBTITLE = (
    "A blog about software engineering, programming languages and technical tinkering"
)

STATIC_PATHS = ["extra", "essays", "images"]

EXTRA_PATH_METADATA = {
    "extra/favicon.ico": {"path": "favicon.ico"},  # and this
    "extra/CNAME": {"path": "CNAME"},
    "extra/LICENSE": {"path": "LICENSE"},
    "extra/README": {"path": "README.md"},
    "essays/graph_db_essay": {"path": "essays/graph_db_essay.html"},
    "extra/slarse.asc": {"path": "gpg/slarse.asc"},
}

PATH = "content"

TIMEZONE = "Europe/Stockholm"

DEFAULT_LANG = "en"

# voidy-bootstrap settings begin
THEME = "voidy-bootstrap"
SIDEBAR = "sidebar.html"
CUSTOM_SIDEBAR_MIDDLES = ("sb_tagcloud.html",)
CUSTOM_ARTICLE_HEADERS = (
    "article_header.html",
    "taglist.html",
)
CUSTOM_INDEX_ARTICLE_HEADERS = (
    "article_header.html",
    "taglist.html",
)
# voidy-bootstrap settings end

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS =

# Social widget

SOCIAL = (
    # ('Twitter', 'https://twitter.com/silarsen',
    #'fab fa-twitter-square fa-fw fa-lg'),
    (
        "LinkedIn",
        "https://www.linkedin.com/in/simon-lars%C3%A9n-b665b3102/",
        "fab fa-linkedin fa-fw fa-lg",
    ),
    ("GitHub", "https://github.com/slarse", "fab fa-github-square fa-fw fa-lg"),
)

FONT_AWESOME_CDN_LINK = {
    "href": "https://use.fontawesome.com/releases/v5.0.13/css/all.css",
    "integrity": "sha384-DNOHZ68U8hZfKXOrtjWvjxusGo9WQnrNx2sqG0tfsghAvtVlRW3tvkXWZh58N9jp",
    "crossorigin": "anonymous",
}

STYLESHEET_FILES = ("pygment.css", "voidybootstrap.css", "search.css")

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# plugins
PLUGIN_PATHS = ["../pelican-plugins"]
PLUGINS = ["tag_cloud", "search"]

CUSTOM_CONTENT_TOP_INDEX = "custom/search.html"
CUSTOM_HTML_HEAD = "custom/head.html"
CUSTOM_SCRIPTS_BASE = "custom/scripts.html"
SEARCH_HTML_SELECTOR = "div#main-container"
