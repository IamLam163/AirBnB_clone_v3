#!/usr/bin/python3
'''A view for State Objects that handles all
default RESTFul API actions
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """This method returns a list of all States"""
    states = storage.all(State)
    return jsonify(
        [state.to_dict() for state in states.values()]
    )


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def by_states_id(state_id):
    """Retrieves states objects by ID"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    return jsonify(
        states.to_dict()
    )


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state method"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """This method creates a a new State"""
    get_json = request.get_json()
    if get_json is None:
        abort(400, 'Not a JSON')
    if get_json['name'] is None:
        abort(404, 'Missing name')
    new_state = State(**get_json)
    new_state.save()
    return jsonify(
        new_state.to_dict()
    ), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """method update states"""
    new_state = storage.get(State, state_id)
    if new_state is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    update = request.get_json()
    attributes = ['id', 'created_at', 'updated_at']
    for key, value in update.items():
        if key not in attributes:
            setattr(new_state, key, value)
    new_state.save()
    return jsonify(new_state.to_dict()), 200
