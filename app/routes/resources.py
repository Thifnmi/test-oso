from flask import Blueprint, g, jsonify, current_app

from app.models import Resource

bp = Blueprint("resources", __name__, url_prefix="/resources")

@bp.route("/<int:resource_id>", methods=["GET"])
def show(resource_id):
    resource = Resource.query.filter_by(id=resource_id)
    return resource