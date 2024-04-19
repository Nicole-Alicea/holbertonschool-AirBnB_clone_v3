#!/usr/bin/python3
'''Here we will be creating the Flask app blueprint'''

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.state import *