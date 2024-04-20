#!/usr/bin/python3
'''Creates a new view for User objects that handles all default
RESTful API actions'''

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    '''Retrieves the list of all User objects'''

    users = storage.all(User).values()
    list_of_users = [user.to_dict() for user in users]

    return jsonify(list_of_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''Retrieves a User object. If a user_id is not linked to any
    User object, it will raise a 404 error'''

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''Deletes a User object'''

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''Creates a User object'''

    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    if 'email' not in data:
        abort(400, 'Missing email')

    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Updates a User object'''

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if request.content_type != 'application/json':
        abort(400, 'Not a JSON')

    data = request.get_json()

    if not data:
        abort(400, 'Not a JSON')

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    storage.save()

    return jsonify(user.to_dict()), 200
