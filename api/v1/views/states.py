#!/usr/bin/python3
""" state file
"""

from flask import jsonify, abort, request, Response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states')
def states():
    """ list all state
    """
    data = [x.to_dict() for x in storage.all(State).values()]
    return jsonify(data)


@app_views.route('/states/<state_id>')
def state(state_id):
    """ get state by id
    """
    data = storage.get(State, state_id)
    if data:
        return data.to_dict()
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ delete insance of item
    """
    get_state = storage.get(State, state_id)
    if get_state:
        get_state.delete()
        del get_state
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """ create new state
    """
    req = request.get_json()
    if req isNone:
        abort(Response("Not a JSON"), 400)

    if req.get('name') is None:
        abort(Response("Missing name"), 400)

    data = State(**req)
    data.save()
    return jsonify(data.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ update instance
    """
    data = storage.get(State, state_id)
    if data is None:
        abort(404)

    req = request.get_json()
    if req is None:
        abort(Response("Not a JSON"), 400)

    req.pop('id', None)
    req.pop('created_at', None)
    req.pop('updated_at', None)

    for k, v in req.items():
        setattr(data, k, v)
    data.save()
    return jsonify(data.to_dict()), 200
