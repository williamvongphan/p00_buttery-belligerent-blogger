# Render register flask template
# app\render\register.py

import flask


def build_page(data=None):
    return flask.render_template('register.html', data=data)
