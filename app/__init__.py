# __init__.py
# This file is part of the Flask-Blog project

import flask
import sqlite3
import utils.util as util
import render.index as render_index

app = flask.Flask(__name__)

@app.route('/')
def index():
    latlong_pair_1 = util.random_latlong()
    latlong_pair_2 = util.random_latlong()
    haversine = util.haversine(
        latlong_pair_1[1],
        latlong_pair_1[0],
        latlong_pair_2[1],
        latlong_pair_2[0]
    )
    return render_index.build_page(latlong_pair_1, latlong_pair_2, haversine)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )