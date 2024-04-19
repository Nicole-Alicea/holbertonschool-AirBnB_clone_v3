#!/usr/bin/python3
'''Creates a new view for State objects that handles all default
RESTful API actions'''

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    '''Retrieves the list of all State objects'''

    states = storage.all(State).values()
    list_of_states = [state.to_dict() for state in states]

    return jsonify(list_of_states)

@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    '''Retrieves a State object. If a state_id is not linked to any
    State object, it will raise a 404 error'''

    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)
    

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State object'''

    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()

        return jsonify({}), 200
    
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a State object'''

    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    
    if not request.get_json():
        return abort(400, 'Not a JSON')
    
    kwargs = request.get_json()

    if 'name' not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()

    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a State object'''

    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    
    state = storage.get(State, state_id)

    if state:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)

        state.save()
        return jsonify(state.to_dict()), 200
    
    else:
        return abort(404)
