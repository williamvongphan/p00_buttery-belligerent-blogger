# Render delete flask template
# app\render\five_hundred.py

import flask


def build_page(data=None):
    return flask.render_template('500.html', data=data)
