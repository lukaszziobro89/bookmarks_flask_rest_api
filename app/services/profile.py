from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
# TODO micro blueprint name change to profile
profile = Blueprint("micro", __name__)


@profile.route('/')
@jwt_required()
def my_profile():
    return jsonify({'micro': 'service'})
