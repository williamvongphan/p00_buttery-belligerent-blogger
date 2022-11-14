# Render index flask template
# app\render\create_blog.py

import flask


def build_page(**kwargs):
    return flask.render_template('newpost.html', **kwargs)
