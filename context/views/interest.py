__author__ = 'robdefeo'

from flask import Blueprint, jsonify, request
from context.data.interest import Interest, TYPE_HEART, TYPE_DETAIL, TYPE_REMOVE, TYPE_AFFILIATE_REDIRECT
import logging

mod_interest = Blueprint('interest', __name__, url_prefix='/interests/')
LOGGER = logging.getLogger(__name__)
interest = Interest()
interest.open_connection()


def create_interest_record(product_id, type_of_interest, active):
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
        active,
        type_of_interest,
        user_id=user_id,
        session_id=session_id
    )

    resp = jsonify({})
    resp.status_code = 201

    return resp


@mod_interest.route('details/<product_id>', methods=['PUT'])
def add_detail(product_id):
    """
    When someone clicks on the show details button
    """
    return create_interest_record(product_id, TYPE_DETAIL, True)

@mod_interest.route('affiliate_redirects/<product_id>', methods=['PUT'])
def add_detail(product_id):
    """
    When someone clicks on the show details button
    """
    return create_interest_record(product_id, TYPE_AFFILIATE_REDIRECT, True)


@mod_interest.route('removes/<product_id>', methods=['PUT'])
def add_remove(product_id):
    """
    When someone clicks on the X button to remove it from the results
    """
    return create_interest_record(product_id, TYPE_REMOVE, True)

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
    """
        when someone clicks on the heart button to save it
    :param product_id:
    :return:
    """
    return create_interest_record(product_id, TYPE_HEART, True)


@mod_interest.route('hearts/<product_id>', methods=['DELETE'])
def remove_heart(product_id):
    """
    When someone clicks on an already hearted button to remove the heart
    :param product_id:
    :return:
    """
    return create_interest_record(product_id, TYPE_HEART, False)
