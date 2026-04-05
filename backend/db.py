import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "shrs",
    "database": "patient_record_system",
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
