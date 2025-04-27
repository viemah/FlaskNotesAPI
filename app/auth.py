from flask import Blueprint, request, jsonify
from . import db
from .models import User
from flask_jwt_extended import create_access_token

bp = Blueprint("auth", __name__)

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"msg": "Username taken"}), 400
    u = User(username=data["username"])
    u.set_password(data["password"])
    db.session.add(u)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    u = User.query.filter_by(username=data["username"]).first()
    if not u or not u.check_password(data["password"]):
        return jsonify({"msg": "Bad credentials"}), 401
    token = create_access_token(identity=u.id)
    return jsonify(access_token=token)
