#!/usr/bin/python3
""" user file
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users')
def all_users():
    """ list all user
    """
    data = [x.to_dict() for x in storage.all(User).values()]
    return jsonify(data)


@app_views.route('/users/<user_id>')
def user(user_id):
    """ get user by id
    """
    data = storage.get(User, user_id)
    if data:
        return jsonify(data.to_dict())
    else:
        abort(404)


@app_views.route('/Users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ delete insance of item
    """
    get_user = storage.get(User, user_id)
    if get_user:
        get_user.delete()
        del get_user
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """ create new user
    """

    req = request.get_json()
    if req is None:
        return ("Not a JSON\n", 400)

    if req.get('name') is None:
        return ("Missing email\n", 400)
    if req.get('password') is None:
        return ("Missing password")
    data = User(**req)
    data.save()
    return jsonify(data.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ update instance
    """
    data = storage.get(User, user_id)
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
