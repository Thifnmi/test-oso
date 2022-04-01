import json
from flask import Blueprint, g, jsonify, current_app, request
from app.models import User
from sqlalchemy.exc import SQLAlchemyError


bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/data/list", methods=["GET"])
def listData():
    return jsonify([item.repr() for item in User.query.all()])


@bp.route("/<int:user_id>", methods=["GET"])
def show(user_id):
    resource = g.session.query(User).filter_by(id=user_id).one_or_none()
    current_app.oso.authorize(g.current_user, "allow", resource)
    return resource.repr()


@bp.route("/create-user", methods=["POST"])
def createUser():
    payload = request.get_json()
    if "email" in payload:
        exists = User.query.filter_by(email=payload["email"]).all()
        if exists:
            return jsonify({
                "message": f"Can not create new user with email {payload['email']}",
                "status": 0,
                "status_code": 400
            }), 400
        user = User(email=payload["email"])
        try:
            g.session.add(user)
            g.session.flush()
            g.session.commit()
            return jsonify({
                "message": f"create user {payload['email']} successful",
                "status": 1,
                "status_code": 201
            }), 201
        except SQLAlchemyError:
            g.session.rollback()
            return jsonify({
                "message": f"Error, rollback data",
                "status": 1,
                "status_code": 400
            }), 400
    return jsonify({
        "message": "missing email in payload",
        "status": 0,
        "status_code": 400
    }), 400

@bp.route("/delete-user", methods=["DELETE"])
def deleteUser():
    payload = request.get_json()
    if "email" in payload:
        exists = User.query.filter_by(email=payload["email"]).first()
        print(exists.repr())
        if exists:
            try:
                # g.session.delete(exists)
                g.session.flush()
                g.session.commit()
                return jsonify({
                    "message": f"delete user {payload['email']} successful",
                    "status": 1,
                    "status_code": 200
                }), 200
            except SQLAlchemyError:
                g.session.rollback()
                return jsonify({
                    "message": f"Error, rollback data",
                    "status": 0,
                    "status_code": 400
                }), 400
        return jsonify({
            "message": f"User {payload['email']} not found",
            "status": 0,
            "status_code": 404,
        }), 404
    return jsonify({
        "message": "missing email in payload",
        "status": 0,
        "status_code": 400
    }), 400
