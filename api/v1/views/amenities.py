#!/usr/bin/python3
"""
Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieves the list of all amenities"""
    amenities = storage.all(Amenity)
    return jsonify(
            [amenity.to_dict() for amenity in amenities.values()]
            )

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenities_by_id(amenity_id):
    """retrieves amenities """
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    return jsonify(
            amenities.to_dict()
            )

#@app_views.route('/amenities/<amenity_id>', method=['DELETE'], strict_slashes=False)
