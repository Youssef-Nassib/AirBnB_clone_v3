#!/usr/bin/python3
"""
This module defines the views for the Review object in the API
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_the_reviews(place_id):
    """
    get the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    get the Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_a_review(review_id):
    """
    delete the Review object
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    create the new Review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    review_data = request.get_json()

    if 'user_id' not in review_data:
        abort(400, description="Missing user_id")
    user = storage.get(User, review_data['user_id'])
    if not user:
        abort(404)

    if 'text' not in review_data:
        abort(400, description="Missing text")

    new_review = Review(**review_data)
    new_review.place_id = place_id
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    update the existing Review
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")
    update_data = request.get_json()

    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in update_data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
