from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import Note

bp = Blueprint("notes", __name__)

@bp.route("/", methods=["GET"])
@jwt_required()
def list_notes():
    uid = get_jwt_identity()
    notes = Note.query.filter_by(user_id=uid).all()
    return jsonify([{"id": n.id, "body": n.body} for n in notes])

@bp.route("/", methods=["POST"])
@jwt_required()
def create_note():
    uid = get_jwt_identity()
    data = request.get_json()
    n = Note(body=data["body"], user_id=uid)
    db.session.add(n)
    db.session.commit()
    return jsonify({"id": n.id, "body": n.body}), 201

@bp.route("/<int:note_id>", methods=["PUT","DELETE"])
@jwt_required()
def modify_note(note_id):
    uid = get_jwt_identity()
    n = Note.query.filter_by(id=note_id, user_id=uid).first_or_404()
    if request.method == "PUT":
        n.body = request.get_json()["body"]
        db.session.commit()
        return jsonify({"id": n.id, "body": n.body})
    else:
        db.session.delete(n)
        db.session.commit()
        return jsonify({"msg": "Deleted"})
