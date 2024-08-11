#!/usr/bin/python3
"""
This module defines the views for the Place object in the API.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity

@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """
    get the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    get the Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    delete the Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    create the new Place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    place_data = request.get_json()

    if 'user_id' not in place_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, place_data['user_id'])
    if not user:
        abort(404)

    if 'name' not in place_data:
        abort(400, description="Missing name")

    new_place = Place(**place_data)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    update an existing Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    update_data = request.get_json()

    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in update_data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves all Place objects depending on the JSON in the request body
    """
    try:
        req_json = request.get_json()
        if req_json is None:
            abort(400, description="Not a JSON")
    except:
        abort(400, description="Not a JSON")

    states = req_json.get('states', [])
    cities = req_json.get('cities', [])
    amenities = req_json.get('amenities', [])

    # If the JSON body is empty or all keys are empty, retrieve all Place objects
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = set()

        # Handle states and cities filtering
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places.update(city.places)

        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.update(city.places)

        # Convert places to list for further filtering with amenities
        places = list(places)

        # Handle amenities filtering
        if amenities:
            filtered_places = []
            for place in places:
                if all(storage.get(Amenity, amenity_id) in place.amenities for amenity_id in amenities):
                    filtered_places.append(place)
            places = filtered_places

    # Convert the Place objects to dictionaries and return them
    places = [place.to_dict() for place in places]
    return jsonify(places)
