from flask import Blueprint, g, jsonify, current_app

from app.models import Permission

bp = Blueprint("permission", __name__, url_prefix="/permission")


@bp.route("/data/list", methods=["GET"])
def lists():
    return jsonify([item.repr() for item in Permission.query.all()])


@bp.route("/<int:permission_id>", methods=["GET"])
def show(permission_id):
    resource = Permission.query.filter_by(id=permission_id).first()
    return resource.repr()