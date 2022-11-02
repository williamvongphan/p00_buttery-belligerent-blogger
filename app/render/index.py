# Render index flask template
# app\render\index.py

import flask
from datetime import datetime

def build_page(latlong_pair_1, latlong_pair_2, haversine):
    time_now = datetime.now()
    return flask.render_template(
        'index.html',
        time_now=time_now,
        haversine=haversine,
        lat1=latlong_pair_1[0],
        lon1=latlong_pair_1[1],
        lat2=latlong_pair_2[0],
        lon2=latlong_pair_2[1],
    )

def build_error_page(error):
    time_now = flask.g.time_now
    return flask.render_template(
        'error.html',
        time_now=time_now,
        error=error
    )