from flask import flash, render_template
from mysql.connector import Error

from backend.auth import login_required
from backend.services.dashboard_service import get_dashboard_data


def register_core_routes(app):
    @app.route("/", endpoint="landing")
    def landing():
        return render_template("landing/landing.html")

    @app.route("/dashboard", endpoint="dashboard")
    @login_required
    def dashboard():
        try:
            counts, recent_appointments, stats = get_dashboard_data()
        except Error as err:
            flash(f"Database error: {err}", "error")
            counts = {"patients": 0, "doctors": 0, "appointments": 0, "records": 0}
            recent_appointments = []
            stats = {}

        return render_template(
            "dashboard/dashboard.html",
            counts=counts,
            recent_appointments=recent_appointments,
            stats=stats,
        )
