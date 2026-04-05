from functools import wraps

from flask import redirect, request, session, url_for


def login_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login", next=request.url))
        return view_func(*args, **kwargs)

    return decorated_function


def authenticate_user(username, password):
    return username == "admin" and password == "password"
