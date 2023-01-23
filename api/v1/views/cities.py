#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def list_city(state_id):
    """method lists all city objects"""
    state = storage.get(State, state_id)
    list_cities = []
    if state is None:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
        """get city by ID"""
        city = storage.get(City, city_id)
        if city is None:
                abort(404)
        return jsonify((city.to_dict()))

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
        """deletes city object by ID"""
        city = storage.get(City, city_id)
        if city is None:
                abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
        """This method creates a new city"""
        get_json = request.get_json()
        state = storage.get(State, state_id)
        if not state:
                abort(404)
        if get_json is None:
                abort(400, 'Not a JSON')
        if get_json['name'] is None:
                abort(400, 'Missing name')

        get_json['state_id'] = state_id
        new_city = City(**get_json)
        new_city.save()
        return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
        """update city object based on the ID"""
        city = storage.get(City, city_id)
        if city is None:
                abort(404)
        get_json = request.get_json()
        if get_json is None:
                abort(400, 'Not a JSON')
        ignore = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in get_json.items():
                if key not in ignore:
                        setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
