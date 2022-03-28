import json
from flask import Blueprint, g, jsonify, current_app, request

from app.models import Role

bp = Blueprint("role", __name__, url_prefix="/role")


@bp.route("/data/list", methods=["GET"])
def listData():
    return jsonify([item.repr() for item in Role.query.all()])
