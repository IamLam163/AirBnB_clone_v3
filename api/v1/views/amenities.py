#!/usr/bin/python3
"""
Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves the list of all amenities"""
    amenities = storage.all(Amenity)
    return jsonify(
        [amenity.to_dict() for amenity in amenities.values()]
    )


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenities_by_id(amenity_id):
    """retrieves amenities """
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(
        amenities.to_dict()
    )


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenities(amenity_id):
    """delete amenities"""
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    storage.delete(amenities)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenities():
    """creates amenities"""
    get_json = request.get_json()
    if get_json is None:
        abort(400, 'Not a JSON')
    if get_json['name'] is None:
        abort(400, 'Missing name')
    new_amenity = Amenity(**get_json)
    new_amenity.save()
    return make_response(jsonify(
        new_amenity.to_dict()
    ), 201)


@app_views.route('amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenities(amenity_id):
    """update amenities by ID"""
    amenity_id = storage.get(Amenity, amenity_id)
    if amenity_id is None:
        abort(404)
    get_json = request.get_json()
    if get_json is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'created_at', 'updated_at']
    for key, values in get_json.items():
        if key not in ignore:
            setattr(amenity_id, key, values)
    amenity_id.save()
    return make_response(jsonify(amenity_id.to_dict()), 200)
