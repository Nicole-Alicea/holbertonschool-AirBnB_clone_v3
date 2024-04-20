#!/usr/bin/python3
'''Here we will create app_views'''

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


# Define a route to return the status of the API
@app_views.route('/status')
def api_status():
    ''' Will return a JSON: "status": "OK" '''
    response = {'status': "OK"}
    return jsonify(response)


# Define a route to retrieve the number of each object by type
@app_views.route('/stats')
def get_stats():
    '''Retrieves the number of each object by type'''
    stats = {
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User),
    }
    return jsonify(stats)
