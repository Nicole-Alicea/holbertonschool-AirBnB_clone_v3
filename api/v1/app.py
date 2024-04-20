#!/usr/bin/python3
'''Here we will be creating an instance of Flask
and registering a blueprint to it'''

from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register the blueprint app_views
app.register_blueprint(app_views)

# Define a teardown method to close the database connection after each request
@app.teardown_appcontext
def teardown(exception):
    '''Performs cleanup operations after each request'''
    storage.close()

# Define an error handler for 404 errors
@app.errorhandler(404)
def not_found(error):
    '''Returns a JSON-formatted 404 status code response'''
    response = {'error': 'Not found'}
    return jsonify(response), 404

# Run the Flask app
if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
