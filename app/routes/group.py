from flask import Blueprint, g, jsonify, current_app

from app.models import Group

bp = Blueprint("group", __name__, url_prefix="/group")

@bp.route("/data/list", methods=["GET"])
def lists():
    return jsonify([item.repr() for item in Group.query.all()])
