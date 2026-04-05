from backend.db import get_db_connection


def list_patients():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patient ORDER BY id DESC")
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_patient_by_id(patient_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patient WHERE id = %s", (patient_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_patient_profile_data(patient_id):
    patient = None
    records = []
    appointments = []

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM patient WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()

        if patient:
            cursor.execute(
                """
                SELECT r.id, r.diagnosis, r.prescription, a.date, d.name as doctor_name
                FROM medical_record r
                JOIN appointment a ON r.appointment_id = a.id
                JOIN doctor d ON a.doctor_id = d.id
                WHERE a.patient_id = %s
                ORDER BY a.date DESC
                """,
                (patient_id,),
            )
            records = cursor.fetchall()

            cursor.execute(
                """
                SELECT a.id, a.date, a.reason, a.status, d.name as doctor_name
                FROM appointment a
                JOIN doctor d ON a.doctor_id = d.id
                WHERE a.patient_id = %s
                ORDER BY a.date DESC
                """,
                (patient_id,),
            )
            appointments = cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

    return patient, records, appointments


def create_patient(name, age, gender, phone, address, description):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patient (name, age, gender, phone, address, description) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, age, gender, phone, address, description),
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_patient(patient_id, name, age, gender, phone, address, description):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE patient SET name=%s, age=%s, gender=%s, phone=%s, address=%s, description=%s WHERE id=%s",
            (name, age, gender, phone, address, description, patient_id),
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_patient(patient_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patient WHERE id = %s", (patient_id,))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
