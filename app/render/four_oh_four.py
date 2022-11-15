# Render delete flask template
# app\render\four_oh_four.py

import flask


def build_page(data=None):
    return flask.render_template('404.html', data=data)
