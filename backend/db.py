import mysql.connector
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "shrs"),
    "database": os.getenv("DB_NAME", "patient_record_system"),
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
