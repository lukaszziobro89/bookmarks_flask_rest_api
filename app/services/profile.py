from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

profile = Blueprint("micro", __name__, url_prefix="/api/v1/bookmarks/profile")


@profile.route('/')
@jwt_required()
def my_profile():
    return jsonify({'micro': 'service'})
