import json
from flask import Blueprint, g, jsonify, current_app, request

from app.models import Role

bp = Blueprint("role", __name__, url_prefix="/role")


@bp.route("/data/list", methods=["GET"])
def listData():
    return jsonify([item.repr() for item in Role.query.all()])


@bp.route("/create-role", methods=["POST"])
def createRole():
    payload = request.get_json()
    if "name" in payload and "description" in payload:
        role = Role(name=f"{payload['name']}_{g.current_user.uuid}", is_custom=True)
        print(role.repr())
    return jsonify({
        "message": "Missing name or description in payload",
        "status": 0,
        "status_code": 400
    })