from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flasgger import swag_from
# TODO micro blueprint name change to profile
profile = Blueprint("micro", __name__, url_prefix="/api/v1/bookmarks/profile")


@profile.route('/')
# @swag_from('./docs/services/profile.yml')
# @jwt_required()
def my_profile():
    return jsonify({'micro': 'service'})
