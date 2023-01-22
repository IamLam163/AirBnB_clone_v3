#!/usr/bin/python3
'''A view for State Objects that handles all 
default RESTFul API actions
'''

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State

@app_views.route('/states', strict_slashes=False)
def list_states():
    """This method returns a list of all States"""
    states = storage.all(State)
    return jsonify(
            [state.to_dict() for state in states.values()]
            )

@app_views.route('/states/<state_id>', strict_slashes=False)
def by_states_id(state_id):
    """Retrieves states objects by ID"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    return jsonify(
            states.to_dict()
            )
@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=True)
def del_states(state_id):
    """Method deletes state objects"""
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    states.delete()
    return jsonify({}), 200

