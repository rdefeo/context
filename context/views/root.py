__author__ = 'robdefeo'

from flask import Blueprint, jsonify, request
mod_root = Blueprint('root', __name__, url_prefix='/')

@mod_root.route('/')
def root():
    resp = jsonify({
        "status": "error",
        "exception": "fake"
    })
    resp.status_code = 500
    return resp