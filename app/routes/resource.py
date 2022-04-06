from flask import Blueprint, g, jsonify, current_app, request

from app.models import Resources

bp = Blueprint("resource", __name__, url_prefix="/resource")


@bp.route("/data/list", methods=["GET"])
def listData():
    return jsonify([item.repr() for item in Resources.query.all()])


@bp.route("/<int:resource_id>", methods=["GET"])
def show(resource_id):
    resource = g.session.query(Resources).filter_by(id=resource_id).one_or_none()
    current_app.oso.authorize(g.current_user, "allow", resource)
    return resource.repr()


@bp.route("/create-permission", methods=["POST"])
def create():
    payload = request.get_json()
    listEndpointRaw = []
    listEndpoint = []
    if "name" in payload and "description" in payload and "resource" in payload and "project" in payload:
        resources = payload["resource"]
        for resource in resources:
            try:
                if resource == "*":
                    key = f"%"
                    endpoints = Resources.query.filter(Resources.endpoint.like(key)).all()
                    for endpoint in endpoints:
                        listEndpointRaw.append(endpoint.repr())
                if resource.split(".")[0] == "*":
                    key = f"%.{resource.split('.')[1]}.{resource.split('.')[2]}"
                    endpoints = Resources.query.filter(Resources.endpoint.like(key)).all()
                    for endpoint in endpoints:
                        listEndpointRaw.append(endpoint.repr())
                if resource.split(".")[1] == "*":
                    key = f"{resource.split('.')[0]}%{resource.split('.')[2]}"
                    endpoints = Resources.query.filter(Resources.endpoint.like(key)).all()
                    for endpoint in endpoints:
                        listEndpointRaw.append(endpoint.repr())
                if resource.split(".")[2] == "*":
                    key = f"{resource.split('.')[0]}.{resource.split('.')[1]}.%"
                    endpoints = Resources.query.filter(Resources.endpoint.like(key)).all()
                    for endpoint in endpoints:
                        listEndpointRaw.append(endpoint.repr())
                if resource.split(".")[0] == "*" and resource.split(".")[1] == "*":
                    key = f"%.{resource.split('.')[2]}"
                    endpoints = Resources.query.filter(Resources.endpoint.like(key)).all()
                    for endpoint in endpoints:
                        listEndpointRaw.append(endpoint.repr())
                if resource.split(".")[0] == "*" and resource.split(".")[2] == "*":
                    key = f"%.{resource.split('.')[1]}.%"
                    endpoints = Resources.query.filter(Resources.endpoint.like(key)).all()
                    for endpoint in endpoints:
                        listEndpointRaw.append(endpoint.repr())
                if resource.split(".")[1] == "*" and resource.split(".")[2] == "*":
                    key = f"{resource.split('.')[0]}.%"
                    endpoints = Resources.query.filter(Resources.endpoint.like(key)).all()
                    for endpoint in endpoints:
                        listEndpointRaw.append(endpoint.repr())
                if resource.split(".")[0] == "*" and resource.split(".")[1] == "*" and resource.split(".")[2] == "*":
                    key = f"%"
                    endpoints = Resources.query.filter(Resources.endpoint.like(key)).all()
                    for endpoint in endpoints:
                        listEndpointRaw.append(endpoint.repr())
                else:
                    endpoint = Resources.query.filter_by(endpoint=resource).first()
                    if endpoint:
                        listEndpointRaw.append(endpoint.repr())
            except:
                pass

        for item in listEndpointRaw:
            if item not in listEndpoint:
                listEndpoint.append(item)

        return jsonify({
            "message": "Success",
            "status": 1,
            "status_code": 201,
            "resource": listEndpoint
        }), 201

    return jsonify({
        "message": "Invalid payload",
        "status": 0,
        "status_code": 400,
        "resource": listEndpoint
    }), 400