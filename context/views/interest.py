__author__ = 'robdefeo'

from flask import Blueprint, jsonify, request
from context.data.interest import Interest, TYPE_HEART
import logging
mod_interest = Blueprint('interest', __name__, url_prefix='/interest/<user_id>/')
LOGGER = logging.getLogger(__name__)

interest = Interest()
interest.open_connection()

@mod_interest.route('heart/<product_id>', methods=['PUT'])
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
