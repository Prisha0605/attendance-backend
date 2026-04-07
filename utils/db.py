import sqlite3
import os
'''
DB_PATH = os.path.join(os.getcwd(), "database", "attendance.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
'''
import sqlite3
import os

def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DB_PATH = os.path.join(BASE_DIR, "..", "database", "attendance.db")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn