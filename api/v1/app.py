#!/usr/bin/python3
"""
create python file
"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.errorhandler(404)
def not_found(error):
    """ 404 page """
    return make_response(jsonify(
        {"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(self):
    storage.close


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
