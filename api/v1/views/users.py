#!/usr/bin/python3
"""
This module defines the views for the User object in the API.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_the_users():
    """
    Retrieves the list of all User objects
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    get a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def deletes_user(user_id):
    """
    delete a User object
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def creates_user():
    """
    creates the new User
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    user_data = request.get_json()
    if 'email' not in user_data:
        abort(400, description="Missing email")
    if 'password' not in user_data:
        abort(400, description="Missing password")
    new_user = User(**user_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    updates the existing User
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    update_data = request.get_json()
    ignored_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in update_data.items():
        if key not in ignored_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
