#!/usr/bin/python3
""" creat a flask app"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def apiStatus():
    """return OK JSON format"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_of_objects():
    """ get the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    num_objcts = {}
    for i in range(len(classes)):
        num_objcts[names[i]] = storage.count(classes[i])

    return jsonify(num_objcts)
