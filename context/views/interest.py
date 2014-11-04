__author__ = 'robdefeo'

from flask import Blueprint, jsonify, request
from context.data.interest import Interest, TYPE_HEART
import logging
mod_interest = Blueprint('interest', __name__, url_prefix='/interests/<user_id>/')
LOGGER = logging.getLogger(__name__)

interest = Interest()
interest.open_connection()

@mod_interest.route('hearts', methods=['GET'])
def get_hearts(user_id):
    items = interest.find(
        user_id,
        TYPE_HEART
    )

    resp = jsonify(items=items)
    resp.status_code = 201
    return resp


@mod_interest.route('hearts/<product_id>', methods=['PUT'])
def add_heart(user_id, product_id):
    interest.upsert(
        product_id,
        user_id,
        True,
        TYPE_HEART
    )
    resp = jsonify({})
    resp.status_code = 201
    return resp

@mod_interest.route('hearts/<product_id>', methods=['DELETE'])
def remove_heart(user_id, product_id):
    interest.upsert(
        product_id,
        user_id,
        False,
        TYPE_HEART
    )
    resp = jsonify({})

    resp.status_code = 204
    return resp
