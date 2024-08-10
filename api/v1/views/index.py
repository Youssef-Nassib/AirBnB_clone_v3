#!/usr/bin/python3
""" creat a flask app"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def apiStatus():
    """return OK JSON format"""
    return jsonify({"status": "OK"})
