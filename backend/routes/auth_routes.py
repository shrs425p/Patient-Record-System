from flask import flash, redirect, render_template, request, session, url_for

from backend.auth import authenticate_user, change_user_password, login_required


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

    @app.route("/change-password", methods=["GET", "POST"], endpoint="change_password")
    @login_required
    def change_password():
        if request.method == "POST":
            current_password = request.form.get("current_password", "")
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not current_password or not new_password or not confirm_password:
                flash("All password fields are required.", "error")
                return redirect(url_for("change_password"))

            if len(new_password) < 6:
                flash("New password must be at least 6 characters long.", "error")
                return redirect(url_for("change_password"))

            if new_password != confirm_password:
                flash("New password and confirm password do not match.", "error")
                return redirect(url_for("change_password"))

            user_id = session.get("user_id")
            if not user_id:
                flash("Session expired. Please log in again.", "error")
                return redirect(url_for("login"))

            ok, message = change_user_password(user_id, current_password, new_password)
            flash(message, "success" if ok else "error")

            if ok:
                return redirect(url_for("dashboard"))

            return redirect(url_for("change_password"))

        return render_template("auth/change_password.html")
