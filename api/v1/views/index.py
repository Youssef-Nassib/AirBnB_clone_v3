#!/usr/bin/python3
""" creat a flask app"""

from flask import jsonif
from api.v1.views import app_views

@app_views.route('/status')
def apiStatus():
    """return OK"""

    response = {'status': "OK"}
    return jsonify(response)