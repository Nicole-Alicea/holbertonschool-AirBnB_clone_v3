#!/usr/bin/python3
"""Flask application for City class/entity"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def retrieves_all_cities(state_id):
    """Returns the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Returns a City object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """Creates a new City object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        abort(400, "Not a JSON")
    if "name" not in city_data:
        abort(400, "Missing name")
    city_data["state_id"] = state_id
    new_city = City(**city_data)
    storage.new(new_city)  # Agrega el nuevo objeto City al almacén
    storage.save()  # Guarda los cambios en el almacén
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Updates a City object by ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        abort(400, "Not a JSON")
    
    # Crear un nuevo diccionario con las claves y valores deseados
    updated_data = {key: value for key, value in city_data.items() 
                    if key not in ["id", "state_id", "created_at", "updated_at"]}
    
    # Actualizar los atributos del objeto City con el nuevo diccionario
    for key, value in updated_data.items():
        setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
