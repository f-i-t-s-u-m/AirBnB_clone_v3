#!/usr/bin/python3
""" state file
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities')
def cities(state_id):
    """ get cities by state id
    """
    data = storage.get(State, state_id)
    cities = [x.to_dict() for x in data.cities]
    if data:
        return jsonify(cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>')
def city(city_id):
    """ get city by id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return city.to_dict()


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ delete insance of item
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    del city
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ create new state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    req = request.get_json()
    if req is None:
        return ("Not a JSON\n", 400)

    if req.get('name') is None:
        return ("Missing name\n", 400)
    req.update({'state_id': state_id})

    data = City(**req)
    data.save()
    return jsonify(data.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ update instance
    """
    data = storage.get(City, city_id)
    if data is None:
        abort(404)

    req = request.get_json()
    if req is None:
        return ("Not a JSON\n", 400)

    req.pop('id', None)
    req.pop('state_id', None)
    req.pop('created_at', None)
    req.pop('updated_at', None)

    for k, v in req.items():
        setattr(data, k, v)
    data.save()
    return jsonify(data.to_dict()), 200
