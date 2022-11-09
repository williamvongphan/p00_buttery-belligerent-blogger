# Render index flask template
# app\render\index.py

import flask


def build_page(**kwargs):
    return flask.render_template('index.html', **kwargs)
