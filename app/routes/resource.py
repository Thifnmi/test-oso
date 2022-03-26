import json
from flask import Blueprint, g, jsonify, current_app

from app.models import Resources

bp = Blueprint("resource", __name__, url_prefix="/resource")


@bp.route("/data/list", methods=["GET"])
def listData():
    return jsonify([item.repr() for item in Resources.query.all()])


@bp.route("/<int:resource_id>", methods=["GET"])
def show(resource_id):
    resource = g.session.query(Resources).filter_by(id=resource_id).first()
    current_app.oso.authorize(g.current_user, "allow", resource)
    return resource.repr()

@bp.route("/list", methods=["GET"])
def list():
    list = current_app.oso.authorized_resources(g.current_user, "allow", Resources)
    return jsonify([item.repr() for item in list])
