#!/usr/bin/python3
'''Here we will create app_views'''

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    ''' Will return a JSON: "status": "OK" '''
    response = {'status': "OK"}
    return jsonify(response)