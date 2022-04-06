from flask import Blueprint, g, jsonify, current_app, request

from app.models import GUMRoleMap, GroupUserMap, Resources, Permission, Role, User

bp = Blueprint("resource", __name__, url_prefix="/resource")


@bp.route("/data/list", methods=["GET"])
def listData():
    return jsonify([item.repr() for item in Resources.query.all()])


@bp.route("/<int:resource_id>", methods=["GET"])
def show(resource_id):
    resource = g.session.query(Resources).filter_by(id=resource_id).one_or_none()
    current_app.oso.authorize(g.current_user, "allow", resource)
    return resource.repr()


def getGUMRoleMapByUserEmail(email):
    exists = User.query.filter_by(email=email).first()
    if exists:
        gum = GroupUserMap.query.filter_by(user_uuid=exists.uuid).first()
        if gum:
            gumrm = GUMRoleMap.query.filter_by(gum_uuid=gum.uuid).first()
            return gumrm
        return None
    return None


def getGUM(email):
    exists = User.query.filter_by(email=email).first()
    if exists:
        gum = GroupUserMap.query.filter_by(user_uuid=exists.uuid).first()
        return gum
    return None


@bp.route("/create-permission", methods=["POST"])
def create():
    payload = request.get_json()
    listEndpointRaw = []
    listEndpoint = []
    gumrm = None
    role = None
    if "user_email" in payload:
        gumrm = getGUMRoleMapByUserEmail(payload["user_email"])

    if "name" in payload and "description" in payload:
        role = Role(name=f"{payload['name']}@{g.current_user.uuid}", description=payload["description"], is_custom=True)
        print(role.repr())
    if "resource" in payload and "project" in payload:
        resources = payload["resource"]
        for resource in resources:
            if payload["resource"][resource] == resource:
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

    if role and listEndpointRaw:
        g.session.add(role)
        g.session.flush()
        g.session.commit()
        if not gumrm:
            gum = getGUM(payload["user_email"])
            gumrm = GUMRoleMap(gum_uuid=gum.uuid, role_uuid=role.uuid)
            print(gumrm.repr())
            g.session.add(gumrm)
            g.session.flush()
            g.session.commit()
        for item in listEndpointRaw:
            if item not in listEndpoint:
                permission = Permission(role_uuid=role.uuid, resource_uuid=item["uuid"], action="allow")
                print(permission.repr())
                g.session.add(permission)
                listEndpoint.append(item)
        g.session.flush()
        g.session.commit()
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


@bp.route("/update-permission", methods=["PUT"])
def update():
    payload = request.get_json()
    listEndpointRaw = []
    listEndpoint = []
    gumrm = None
    role = None
    if "user_email" in payload:
        gumrm = getGUMRoleMapByUserEmail(payload["user_email"])

    if "name" in payload and "description" in payload:
        role = Role.query.filter_by(name=f"{payload['name']}@{g.current_user.uuid}", description=payload["description"], is_custom=True).first()

    if "resource" in payload and "project" in payload:
        resources = payload["resource"]
        for resource in resources:
            if payload["resource"][resource] == resource:
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

    if gumrm and role and listEndpointRaw:
        for item in listEndpointRaw:
            if item not in listEndpoint:
                if not Permission.query.filter_by(role_uuid=role.uuid, resource_uuid=item["uuid"], action="allow").all():
                    permission = Permission(role_uuid=role.uuid, resource_uuid=item["uuid"], action="allow")
                    g.session.add(permission)
                listEndpoint.append(item)
        g.session.flush()
        g.session.commit()
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