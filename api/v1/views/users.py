#!/usr/bin/python3
"""object that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """retrieve list of Users"""
    users = storage.all(User)
    return jsonify(
            [user.to_dict() for user in users.values()]
            )


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """method get user by ID"""
    users = storage.get(User, user_id)
    if not users:
        abort(404)
    return jsonify(users.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """method deltes a user"""
    user = storage.get(User, user_id)
    if user is None:
        error(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_users():
    """method creates users"""
    get_json = request.get_json()
    if get_json is None:
        abort(400, 'Not a JSON')
    if get_json['email'] is None:
        abort(400, 'Missing email')
    if get_json['password'] is None:
        abort(400, 'Misssing password')

    new_user = User(**get_json)
    new_user.save()
    return jsonify(
            new_user.to_dict()
            ), 201

