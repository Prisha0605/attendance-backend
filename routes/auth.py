from flask import Blueprint, request, jsonify
from utils.db import get_db
from utils.jwt_helper import generate_token

auth_bp = Blueprint("auth", __name__)

# STUDENT LOGIN
@auth_bp.route("/login/student", methods=["POST"])
def student_login():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT student_id FROM student WHERE email=? AND password=?",
                (data["email"], data["password"]))

    user = cur.fetchone()
    conn.close()

    if user:
        token = generate_token(user["student_id"], "student")
        return jsonify({"token": token, "role": "student"})

    return jsonify({"error": "Invalid credentials"}), 401


# TEACHER LOGIN
@auth_bp.route("/login/teacher", methods=["POST"])
def teacher_login():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT teacher_id FROM teacher WHERE email=? AND password=?",
                (data["email"], data["password"]))

    user = cur.fetchone()
    conn.close()

    if user:
        token = generate_token(user["teacher_id"], "teacher")
        return jsonify({"token": token, "role": "teacher"})

    return jsonify({"error": "Invalid credentials"}), 401