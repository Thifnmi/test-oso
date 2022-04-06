from flask import Blueprint, g, jsonify, current_app, request

from app.models import Group

bp = Blueprint("group", __name__, url_prefix="/group")

@bp.route("/data/list", methods=["GET"])
def lists():
    return jsonify([item.repr() for item in Group.query.all()])

@bp.route("/create-group", methods=["POST"])
def create():
    payload = request.get_json()
    