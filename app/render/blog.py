# Render index flask template
# app\render\blog.py

import flask


def build_page(**kwargs):
    return flask.render_template('blog.html', **kwargs)
