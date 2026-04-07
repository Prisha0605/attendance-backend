from flask import Flask
from flask_jwt_extended import JWTManager
from config import SECRET_KEY, JWT_SECRET_KEY

from routes.auth import auth_bp
from routes.student import student_bp
from routes.teacher import teacher_bp
from routes.attendance import attendance_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

jwt = JWTManager(app)

# Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(attendance_bp)

@app.route("/")
def home():
    return {"message": "Backend running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)