#!/usr/bin/python3
""" a place file
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places')
def places(city_id):
    """ get places by city id
    """
    data = storage.get(City, city_id)
    places = [x.to_dict() for x in data.places]
    if data:
        return jsonify(places)
    else:
        abort(404)


@app_views.route('/places/<place_id>')
def place(place_id):
    """ get place by id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return place.to_dict()


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ delete insance of item
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    del place
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(place_id):
    """ create new place
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    req = request.get_json()
    if req is None:
        return ("Not a JSON\n", 400)
    if req.get('user_id') is None:
        return ("Missing user_id")
    user = storage.get(User, req.get('user_id'))
    if not user:
        abort(404)
    if req.get('name') is None:
        return ("Missing name\n", 400)
    req.update({'city_id': city_id, 'user_id': req.get('user_id')})

    data = Place(**req)
    data.save()
    return jsonify(data.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ update instance
    """
    data = storage.get(Place, place_id)
    if data is None:
        abort(404)

    req = request.get_json()
    if req is None:
        return ("Not a JSON\n", 400)

    req.pop('id', None)
    req.pop('user_id', None)
    req.pop('city_id', None)
    req.pop('created_at', None)
    req.pop('updated_at', None)

    for k, v in req.items():
        setattr(data, k, v)
    data.save()
    return jsonify(data.to_dict()), 200
