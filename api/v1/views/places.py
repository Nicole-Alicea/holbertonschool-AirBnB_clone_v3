#!/usr/bin/python3
"""Flask application for Place class/entity"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def retrieves_all_places(city_id):
    """Returns the list of all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = city.places
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Returns an object by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes an object by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Creates an object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")

    if "user_id" not in place_data:
        abort(400, "Missing user_id")

    user = storage.get(User, place_data.get("user_id"))
    if not user:
        abort(404)

    if "name" not in place_data:
        abort(400, "Missing name")

    place_data["city_id"] = city_id
    place = Place(**place_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates an object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place_data = request.get_json()
    if not place_data:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in place_data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
