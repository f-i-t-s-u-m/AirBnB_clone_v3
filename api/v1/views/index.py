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
    classes = {"Amenity": "amenities", "City": "cities",
               "Place": "places", "Review": "reviews",
               "State": "states", "User": "users"}

    data = {}
    for key, val in classes.items():
        data[val] = storage.count(key)

    return jsonify(data)


@app_views.route('/status', strict_slashes=False)
def status():
    """ server status """
    return jsonify({'status': 'OK'})
