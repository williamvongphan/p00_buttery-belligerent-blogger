# Render delete flask template
# app\render\delete.py

import flask


def build_page(data=None):
    return flask.render_template('delete.html', data=data)
