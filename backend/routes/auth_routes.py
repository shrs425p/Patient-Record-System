from flask import flash, redirect, render_template, request, session, url_for

from backend.auth import authenticate_user


def register_auth_routes(app):
    @app.route("/login", methods=["GET", "POST"], endpoint="login")
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = authenticate_user(username, password)
            if user:
                session["logged_in"] = True
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                flash("Successfully logged in.", "success")
                next_page = request.args.get("next")
                return redirect(next_page or url_for("dashboard"))

            flash("Invalid credentials.", "error")

        return render_template("auth/login.html")

    @app.route("/logout", endpoint="logout")
    def logout():
        session.pop("logged_in", None)
        session.pop("user_id", None)
        session.pop("username", None)
        flash("You have been logged out.", "success")
        return redirect(url_for("login"))
