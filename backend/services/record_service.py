from backend.db import get_db_connection


def list_records(search=""):
    record_list = []
    appointment_list = []

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        base_query = """
            SELECT mr.id, mr.diagnosis, mr.prescription,
                   a.id AS appointment_id, a.date,
                   p.id AS patient_id, p.name AS patient_name,
                   d.name AS doctor_name
            FROM medical_record mr
            JOIN appointment a ON mr.appointment_id = a.id
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
        """

        if search:
            cursor.execute(
                base_query + " WHERE p.name LIKE %s ORDER BY mr.id DESC",
                (f"%{search}%",),
            )
        else:
            cursor.execute(base_query + " ORDER BY mr.id DESC")

        record_list = cursor.fetchall()

        cursor.execute(
            """
            SELECT a.id, a.date, p.name AS patient_name, d.name AS doctor_name
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            JOIN doctor d ON a.doctor_id = d.id
            LEFT JOIN medical_record mr ON mr.appointment_id = a.id
            WHERE mr.id IS NULL
            ORDER BY a.date DESC, a.id DESC
            """
        )
        appointment_list = cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return record_list, appointment_list


def get_record_by_id(record_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM medical_record WHERE id = %s", (record_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def list_appointments_for_record_select():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT a.id, p.name as patient_name, a.date
            FROM appointment a
            JOIN patient p ON a.patient_id = p.id
            ORDER BY a.date DESC
            """
        )
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def create_record(appointment_id, diagnosis, prescription):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO medical_record (appointment_id, diagnosis, prescription) VALUES (%s, %s, %s)",
            (appointment_id, diagnosis, prescription),
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_record(record_id, appointment_id, diagnosis, prescription):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE medical_record SET appointment_id=%s, diagnosis=%s, prescription=%s WHERE id=%s",
            (appointment_id, diagnosis, prescription, record_id),
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_record(record_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM medical_record WHERE id = %s", (record_id,))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
