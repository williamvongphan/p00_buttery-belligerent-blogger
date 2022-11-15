# Render index flask template
# app\render\delete_blog.py

import flask


def build_page(**kwargs):
    return flask.render_template('delete_blog.html', **kwargs)