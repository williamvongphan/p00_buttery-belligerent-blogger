# Render login flask template
# app\render\login.py

import flask


def build_page(data=None):
    return flask.render_template('login.html', data=data)
