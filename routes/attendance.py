from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from services.attendance_service import process_attendance

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/mark_attendance", methods=["POST"])
@jwt_required()
def mark_attendance():
    claims = get_jwt()
    student_id = get_jwt_identity()

    if claims.get("role") != "student":
        return jsonify({"error": "Unauthorized"}), 403

    face_match = request.json.get("face_match")

    if face_match is not True:
        return jsonify({
            "status": "ABSENT",
            "message": "Face mismatch"
        })

    course_id = request.json.get("course_id")
    ble = request.json.get("ble_readings")

    status, message = process_attendance(student_id, course_id, ble)

    return jsonify({
        "status": status,
        "message": message
    })