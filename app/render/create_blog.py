# Render index flask template
# app\render\create_blog.py

import flask


def build_page(**kwargs):
    return flask.render_template('create_blog.html', **kwargs)
