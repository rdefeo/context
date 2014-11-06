__author__ = 'robdefeo'

from flask import Blueprint, jsonify, request
import logging
from context.data.log import Log
mod_log = Blueprint('log', __name__, url_prefix='/logs/')
LOGGER = logging.getLogger(__name__)

data_access_log = Log()
data_access_log.open_connection()

@mod_log.route('<_type>', methods=['GET'])
def test(_type):
    return jsonify({})

@mod_log.route('<_type>', methods=['POST'])
def log(_type):
    j = request.get_json(force=True)
    data_access_log.insert(_type, j)

    return jsonify({})

