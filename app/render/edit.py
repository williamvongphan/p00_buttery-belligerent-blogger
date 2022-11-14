# Render index flask template
# app\render\edit.py

import flask


def build_page(**kwargs):
    return flask.render_template('edit.html', **kwargs)