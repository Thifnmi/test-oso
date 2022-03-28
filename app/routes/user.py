from flask import Blueprint, g, jsonify, current_app

from app.models import User

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/data/list", methods=["GET"])
def listData():
    return jsonify([item.repr() for item in User.query.all()])

@bp.route("/<int:user_id>", methods=["GET"])
def show(user_id):
    resource = g.session.query(User).filter_by(id=user_id).one_or_none()
    current_app.oso.authorize(g.current_user, "allow", resource)
    return resource.repr()