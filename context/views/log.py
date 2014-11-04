__author__ = 'robdefeo'

from flask import Blueprint, jsonify, request
import logging
mod_log = Blueprint('log', __name__, url_prefix='/log/')
LOGGER = logging.getLogger(__name__)

@mod_log.route('/load_more')
def log_something():
    j = request.get_json(force=True)

