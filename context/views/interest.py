__author__ = 'robdefeo'

from flask import Blueprint, jsonify, request
from context.data.interest import Interest, TYPE_HEART, TYPE_DETAIL, TYPE_REMOVE
import logging

mod_interest = Blueprint('interest', __name__, url_prefix='/interests/')
LOGGER = logging.getLogger(__name__)
interest = Interest()
interest.open_connection()


@mod_interest.route('details/<product_id>', methods=['PUT'])
def add_detail(product_id):
    """
    When someone clicks on the show details button
    """
    payload = request.get_json(force=True)
    user_id = None
    session_id = None
    if "user_id" in payload:
        user_id = payload["user_id"]
    if "session_id" in payload:
        session_id = payload["session_id"]

    if user_id is None and session_id is None:
        resp = jsonify(
            {
                "status": "error",
                "message": "missing user_id / session_id"
            }
        )
        resp.status_code = 412
        return resp

    interest.upsert(
        product_id,
        True,
        TYPE_DETAIL,
        user_id=user_id,
        session_id=session_id
    )
    resp = jsonify({})
    resp.status_code = 201
    return resp


@mod_interest.route('removes/<product_id>', methods=['PUT'])
def add_remove(product_id):
    """
    When someone clicks on the show details button
    """
    payload = request.get_json(force=True)
    user_id = None
    session_id = None
    if "user_id" in payload:
        user_id = payload["user_id"]
    if "session_id" in payload:
        session_id = payload["session_id"]

    if user_id is None and session_id is None:
        resp = jsonify(
            {
                "status": "error",
                "message": "missing user_id / session_id"
            }
        )
        resp.status_code = 412
        return resp

    interest.upsert(
        product_id,
        True,
        TYPE_REMOVE,
        user_id=user_id,
        session_id=session_id
    )
    resp = jsonify({})
    resp.status_code = 201
    return resp


@mod_interest.route('hearts', methods=['GET'])
def get_hearts():
    user_id = request.args.get('user_id')
    session_id = request.args.get('session_id')

    if user_id is None and session_id is None:
        resp = jsonify(
            {
                "status": "error",
                "message": "missing user_id / session_id"
            }
        )
        resp.status_code = 412
        return resp

    items = interest.find(
        TYPE_HEART,
        session_id=session_id,
        user_id=user_id
    )

    resp = jsonify(items=items)
    resp.status_code = 201
    return resp


@mod_interest.route('hearts/<product_id>', methods=['PUT'])
def add_heart(product_id):
    payload = request.get_json(force=True)
    user_id = None
    session_id = None
    if "user_id" in payload:
        user_id = payload["user_id"]
    if "session_id" in payload:
        session_id = payload["session_id"]

    if user_id is None and session_id is None:
        resp = jsonify(
            {
                "status": "error",
                "message": "missing user_id / session_id"
            }
        )
        resp.status_code = 412
        return resp

    interest.upsert(
        product_id,
        True,
        TYPE_HEART,
        user_id=user_id,
        session_id=session_id
    )
    resp = jsonify({})
    resp.status_code = 201
    return resp

@mod_interest.route('hearts/<product_id>', methods=['DELETE'])
def remove_heart(product_id):
    payload = request.get_json(force=True)
    user_id = None
    session_id = None
    if "user_id" in payload:
        user_id = payload["user_id"]
    if "session_id" in payload:
        session_id = payload["session_id"]

    if user_id is None and session_id is None:
        resp = jsonify(
            {
                "status": "error",
                "message": "missing user_id / session_id"
            }
        )
        resp.status_code = 412
        return resp

    interest.upsert(
        product_id,
        False,
        TYPE_HEART,
        user_id=user_id,
        session_id=session_id
    )
    resp = jsonify({})

    resp.status_code = 204
    return resp
