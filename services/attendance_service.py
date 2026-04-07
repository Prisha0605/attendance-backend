import json
from datetime import datetime
from utils.db import get_db
from services.ble_service import detect_classroom_from_ble


def process_attendance(student_id, course_id, ble_json):
    conn = get_db()
    cur = conn.cursor()

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    current_time = now.time()

    # ---------------- CHECK ACTIVE SESSION ----------------
    cur.execute("""
        SELECT session_id, classroom_id, start_time, end_time
        FROM class_session
        WHERE course_id=? AND session_date=? AND is_active=1
    """, (course_id, today))

    session = cur.fetchone()

    if not session:
        conn.close()
        return "ABSENT", "No active session"

    session_id = session["session_id"]
    classroom_id = session["classroom_id"]

    # ---------------- TIME CHECK (FINAL FIX) ----------------
    if session["start_time"]:
        start = datetime.strptime(session["start_time"], "%H:%M:%S").time()

        # If end_time exists → strict window
        if session["end_time"]:
            end = datetime.strptime(session["end_time"], "%H:%M:%S").time()

            if not (start <= current_time <= end):
                conn.close()
                return "ABSENT", "Outside class time"

        # If end_time NOT set → allow only after start
        else:
            if current_time < start:
                conn.close()
                return "ABSENT", "Session not started yet"

    # ---------------- BLE CHECK ----------------
    ble_readings = json.loads(ble_json)

    minor, rssi = detect_classroom_from_ble(ble_readings)

    if not minor:
        conn.close()
        return "ABSENT", "No BLE detected"

    cur.execute("""
        SELECT classroom_id FROM classroom
        WHERE beacon_minor=?
    """, (minor,))

    room = cur.fetchone()

    if not room or room["classroom_id"] != classroom_id:
        conn.close()
        return "ABSENT", "Wrong classroom"

    # ---------------- SAVE ATTENDANCE ----------------
    cur.execute("""
        INSERT OR IGNORE INTO attendance
        (student_id, session_id, status, marked_at, classroom_id,rssi)
        VALUES (?, ?, ?, ?, ?,?)
    """, (student_id, session_id, "PRESENT", datetime.now(),classroom_id,rssi))

    conn.commit()
    conn.close()

    return "PRESENT", "Attendance marked"