from functools import wraps
import os

from flask import redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from backend.db import get_db_connection


def login_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.url))
        return view_func(*args, **kwargs)

    return decorated_function


def initialize_auth_storage():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        default_username = os.getenv("DEFAULT_ADMIN_USER", "admin")
        default_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "password")

        cursor.execute("SELECT id FROM users WHERE username = %s", (default_username,))
        existing = cursor.fetchone()

        if not existing:
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (default_username, generate_password_hash(default_password)),
            )

        conn.commit()
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def authenticate_user(username, password):
    if not username or not password:
        return None

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return None

        if check_password_hash(user["password_hash"], password):
            return {"id": user["id"], "username": user["username"]}
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
