#!/usr/bin/python3
'''Creates a new view for State objects that handles all default
RESTful API actions'''

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''Retrieves the list of all State objects'''

    states = storage.all(State).values()
    list_of_states = [state.to_dict() for state in states]

    return jsonify(list_of_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''Retrieves a State object. If a state_id is not linked to any
    State object, it will raise a 404 error'''

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    return jsonify(state.to_dict())
    

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State object'''

    state = storage.get(State, state_id)

    if not state:
        abort(404)
    
    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a State object'''

    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    
    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')
    
    if 'name' not in data:
        abort(400, 'Missing name')

    state = State(**data)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a State object'''

    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')
    
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    storage.save()
    
    return jsonify(state.to_dict()), 200
