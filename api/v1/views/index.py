#!/usr/bin/python3
"""
index file
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """ server status """
    return jsonify({'status': 'OK'})
