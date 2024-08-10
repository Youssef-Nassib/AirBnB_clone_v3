#!/usr/bin/python3
""" creat a flask app"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def apiStatus():
    """return OK JSON format"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stat():
    """methode to get stats"""

    stats = {
        "Amenity": storage.count("Amenity"),
        "City": storage.count("City"),
        "Place": storage.count("Place"),
        "Review": storage.count("Review"),
        "State": storage.count("State"),
        "User": storage.count("User")
    }

    return jsonify(stats)
