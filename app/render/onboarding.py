# Render onboarding flask template
# app\render\onboarding.py

import flask


def build_page(data=None):
    return flask.render_template('onboarding.html', data=data)
