from flask import Blueprint, g, jsonify, current_app

from app.models import User

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/<int:user_id>", methods=["GET"])
def show(user_id):
    resource = User.query.filter_by(id=user_id)
    return resource