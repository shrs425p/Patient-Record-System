from backend.db import get_db_connection


def list_doctors():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctor ORDER BY id DESC")
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


def get_doctor_by_id(doctor_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM doctor WHERE id = %s", (doctor_id,))
        return cursor.fetchone()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def create_doctor(name, specialty, phone, email, description):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctor (name, specialty, phone, email, description) VALUES (%s, %s, %s, %s, %s)",
            (name, specialty, phone, email, description),
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_doctor(doctor_id, name, specialty, phone, email, description):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE doctor SET name=%s, specialty=%s, phone=%s, email=%s, description=%s WHERE id=%s",
            (name, specialty, phone, email, description, doctor_id),
        )
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_doctor(doctor_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctor WHERE id = %s", (doctor_id,))
        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
