from backend.db import get_db_connection


def list_appointments():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT a.id, a.date, a.reason,
                   CASE
                       WHEN a.status = 'Completed' THEN 'Completed'
                       WHEN a.status = 'Cancelled' OR a.date < CURDATE() THEN 'Cancelled'
                       ELSE 'Pending'
                   END AS status,
                   p.name AS patient_name,
                   d.name AS doctor_name,
                   d.specialty
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
            ORDER BY a.date DESC, a.id DESC
            """
        )
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def list_patients_for_select():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM patient ORDER BY name")
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def list_doctors_for_select():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, specialty FROM doctor ORDER BY name")
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_appointment_by_id(appointment_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT a.*,
                   a.status AS raw_status,
                   CASE
                       WHEN a.status = 'Completed' THEN 'Completed'
                       WHEN a.status = 'Cancelled' OR a.date < CURDATE() THEN 'Cancelled'
                       ELSE 'Pending'
                   END AS status
            FROM appointment a
            WHERE a.id = %s
            """,
            (appointment_id,),
        )
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def create_appointment(patient_id, doctor_id, date_value, reason):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointment (patient_id, doctor_id, date, reason) VALUES (%s, %s, %s, %s)",
            (patient_id, doctor_id, date_value, reason),
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_appointment(appointment_id, patient_id, doctor_id, date_value, reason, status):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Keep DB compatibility: legacy enum may still store 'Scheduled'.
        db_status = "Scheduled" if status == "Pending" else status

        cursor.execute(
            "UPDATE appointment SET patient_id=%s, doctor_id=%s, date=%s, reason=%s, status=%s WHERE id=%s",
            (patient_id, doctor_id, date_value, reason, db_status, appointment_id),
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_appointment(appointment_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointment WHERE id = %s", (appointment_id,))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
