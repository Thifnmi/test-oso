from flask import Blueprint, g, jsonify, current_app

from app.models import User

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/<int:user_id>", methods=["GET"])
def show(user_id):
    resource = g.session.query(User).filter_by(id=user_id).one_or_none()
    current_app.oso.authorize(g.current_user, "allow", resource)

    return resource.repr()