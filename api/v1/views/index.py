#!/usr/bin/python3
'''Here we will create app_views'''

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def api_status():
    ''' Will return a JSON: "status": "OK" '''
    response = {'status': "OK"}
    return jsonify(response)


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
