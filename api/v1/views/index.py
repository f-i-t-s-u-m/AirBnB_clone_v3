#!/usr/bin/python3
"""
index file
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/stats', strict_slashes=False)
def stats():
    """ show stats of records
    """
    classes = {"Amenity", "BaseModel", "City",
           "Place", "Review", "State", "User"}

    data = {}
    for val in classes:
        data[val.lower()] = storage.count(val)

    return jsonify(data)


@app_views.route('/status', strict_slashes=False)
def status():
    """ server status """
    return jsonify({'status': 'OK'})
