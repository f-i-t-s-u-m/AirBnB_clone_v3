#!/usr/bin/python3
""" state file
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities')
def amenities():
    """ list all amenities
    """
    data = [x.to_dict() for x in storage.all(Amenity).values()]
    return jsonify(data)


@app_views.route('/amenities/<amenity_id>')
def amenity(amenity_id):
    """ get amenities by id
    """
    data = storage.get(Amenity, amenity_id)
    if data:
        return jsonify(data.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ delete insance of item
    """
    get_amenity = storage.get(Amenity, amenity_id)
    if get_amenity:
        get_amenity.delete()
        del get_amenity
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """ create new amenities
    """

    req = request.get_json()
    if req is None:
        return ("Not a JSON\n", 400)

    if req.get('name') is None:
        return ("Missing name\n", 400)

    data = Amenity(**req)
    data.save()
    return jsonify(data.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ update instance
    """
    data = storage.get(Amenity, amenity_id)
    if data is None:
        abort(404)

    req = request.get_json()
    if req is None:
        return ("Not a JSON\n", 400)

    req.pop('id', None)
    req.pop('created_at', None)
    req.pop('updated_at', None)

    for k, v in req.items():
        setattr(data, k, v)
    data.save()
    return jsonify(data.to_dict()), 200
