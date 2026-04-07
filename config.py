import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, "database", "attendance.db")

SECRET_KEY = "super-secret-key"
JWT_SECRET_KEY = "jwt-secret-key"
