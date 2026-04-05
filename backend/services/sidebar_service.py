from datetime import date

from backend.db import get_db_connection


def get_sidebar_stats():
    stats = {"patient_count": 0, "appointment_today_count": 0}
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) as count FROM patient")
        result = cursor.fetchone()
        stats["patient_count"] = result["count"] if result else 0

        today = date.today().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT COUNT(*) as count FROM appointment WHERE date = %s AND status != 'Cancelled'",
            (today,),
        )
        result = cursor.fetchone()
        stats["appointment_today_count"] = result["count"] if result else 0
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return stats
