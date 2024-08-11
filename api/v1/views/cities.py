#!/usr/bin/python3
"""
This module defines the views for the City object in the API.
It handles all default RESTful API actions related to City objects.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves a list of all City objects associated with a given State.

    Args:
        state_id (str): The ID of the State to retrieve cities for.

    Returns:
        Response: A JSON list of City objects.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by its ID.

    Args:
        city_id (str): The ID of the City to retrieve.

    Returns:
        Response: A JSON representation of the City object.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by its ID.

    Args:
        city_id (str): The ID of the City to delete.

    Returns:
        Response: An empty JSON response with HTTP status code 200.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object within a given State.

    Args:
        state_id (str): The ID of the State where the City will be created.

    Returns:
        Response: A JSON representation of the newly created City object with HTTP status code 201.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    city_data = request.get_json()
    if 'name' not in city_data:
        abort(400, description="Missing name")
    city_data['state_id'] = state_id
    new_city = City(**city_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates an existing City object by its ID.

    Args:
        city_id (str): The ID of the City to update.

    Returns:
        Response: A JSON representation of the updated City object with HTTP status code 200.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    update_data = request.get_json()
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in update_data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
