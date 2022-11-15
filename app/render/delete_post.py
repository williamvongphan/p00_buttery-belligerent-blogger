# Render delete flask template
# app\render\delete_post.py

import flask


def build_page(data=None):
    return flask.render_template('delete_blog.html', data=data)
