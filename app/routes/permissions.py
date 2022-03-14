from flask import Blueprint, g, jsonify, current_app

from app.models import Permission

bp = Blueprint("permissions", __name__, url_prefix="/permission")

@bp.route("/<int:permission_id>", methods=["GET"])
def show(permission_id):
    resource = Permission.query.filter_by(id=permission_id)
    return resource