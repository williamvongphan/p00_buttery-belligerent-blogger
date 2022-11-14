# Render index flask template
# app\render\homepage.py

import flask

def build_page(**kwargs):
    return flask.render_template('homepage.html', **kwargs)
