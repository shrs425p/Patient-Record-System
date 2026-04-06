from datetime import datetime

from backend.db import get_db_connection


def get_dashboard_data():
    counts = {"patients": 0, "doctors": 0, "appointments": 0, "records": 0}
    recent_appointments = []
    stats = {"today_full": datetime.now().strftime("%A, %d %B %Y")}

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM patient")
        counts["patients"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM doctor")
        counts["doctors"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM appointment")
        counts["appointments"] = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM medical_record")
        counts["records"] = cursor.fetchone()["total"]

        cursor.execute(
            """
            SELECT a.id,
                   p.name as patient_name,
                   d.name as doctor_name,
                   a.date,
                   CASE
                       WHEN a.status = 'Completed' THEN 'Completed'
                       WHEN a.status = 'Cancelled' OR a.date < CURDATE() THEN 'Cancelled'
                       ELSE 'Pending'
                   END AS status
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
            WHERE a.date >= CURDATE() AND a.status NOT IN ('Completed', 'Cancelled')
            ORDER BY a.date ASC
            LIMIT 5
            """
        )
        recent_appointments = cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return counts, recent_appointments, stats
