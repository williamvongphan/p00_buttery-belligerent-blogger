# Render index flask template
# app\render\post.py

import flask


def build_page(**kwargs):
    return flask.render_template('post.html', **kwargs)
