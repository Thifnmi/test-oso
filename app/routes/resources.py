import json
from flask import Blueprint, g, jsonify, current_app

from app.models import Repository

bp = Blueprint("resources", __name__, url_prefix="/resource")

@bp.route("/<int:resource_id>", methods=["GET"])
def show(resource_id):
    resource = g.session.query(Repository).filter_by(id=resource_id).first()
    current_app.oso.authorize(g.current_user, "allow", resource)
    return resource.repr()

@bp.route("/list", methods=["GET"])
def list():
    list = current_app.oso.authorized_resources(g.current_user, "allow", Repository)
    return jsonify([item.repr() for item in list])
