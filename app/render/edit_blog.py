# Render index flask template
# app\render\edit_blog.py

import flask


def build_page(**kwargs):
    return flask.render_template('edit_blog.html', **kwargs)