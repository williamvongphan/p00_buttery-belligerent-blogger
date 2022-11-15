# Render index flask template
# app\render\edit_post.py

import flask


def build_page(**kwargs):
    return flask.render_template('edit_post.html', **kwargs)