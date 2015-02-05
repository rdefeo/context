__author__ = 'robdefeo'

from flask import Blueprint, jsonify, request
import logging
from context.data.log import Log
from datetime import datetime

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
    date = datetime.now().isoformat()
    j["timestamp"] = date
    data_access_log.insert(_type, j)

    return jsonify({})

