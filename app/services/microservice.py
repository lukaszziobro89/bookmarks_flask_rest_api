from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

micro = Blueprint("micro", __name__, url_prefix="/api/v1/bookmarks/micro")


@micro.route('/abc')
@jwt_required()
def micro_abc():
    return jsonify({'micro': 'service'})
