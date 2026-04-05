from flask import flash, redirect, render_template, request, url_for
from mysql.connector import Error

from backend.auth import login_required
from backend.services.doctor_service import (
    create_doctor,
    delete_doctor,
    get_doctor_by_id,
    list_doctors,
    update_doctor,
)


def register_doctor_routes(app):
    @app.route("/doctors", endpoint="doctors")
    @login_required
    def doctors():
        doctor_list = []
        try:
            doctor_list = list_doctors()
        except Error as err:
            flash(f"Database error: {err}", "error")

        return render_template("doctors/doctors.html", doctors=doctor_list)

    @app.route("/doctors/add", methods=["GET", "POST"], endpoint="add_doctor")
    @login_required
    def add_doctor_route():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            specialty = request.form.get("specialty", "").strip()
            phone = request.form.get("phone", "").strip()
            email = request.form.get("email", "").strip()
            description = request.form.get("description", "").strip()

            if not name or not specialty:
                flash("Name and specialty are required.", "error")
                return redirect(url_for("add_doctor"))

            try:
                create_doctor(name, specialty, phone, email, description)
                flash("Doctor added successfully.", "success")
                return redirect(url_for("doctors"))
            except Error as err:
                flash(f"Database error: {err}", "error")

        return render_template("doctors/add_doctor.html")

    @app.route("/doctors/edit/<int:doctor_id>", methods=["GET", "POST"], endpoint="edit_doctor")
    @login_required
    def edit_doctor_route(doctor_id):
        try:
            if request.method == "POST":
                name = request.form.get("name", "").strip()
                specialty = request.form.get("specialty", "").strip()
                phone = request.form.get("phone", "").strip()
                email = request.form.get("email", "").strip()
                description = request.form.get("description", "").strip()

                if not name or not specialty:
                    flash("Name and specialty are required.", "error")
                    return redirect(url_for("edit_doctor", doctor_id=doctor_id))

                update_doctor(doctor_id, name, specialty, phone, email, description)
                flash("Doctor updated successfully.", "success")
                return redirect(url_for("doctors"))

            doctor = get_doctor_by_id(doctor_id)
            if not doctor:
                flash("Doctor not found.", "error")
                return redirect(url_for("doctors"))

            return render_template("doctors/edit_doctor.html", doctor=doctor)
        except Error as err:
            flash(f"Database error: {err}", "error")
            return redirect(url_for("doctors"))

    @app.route("/doctors/delete/<int:doctor_id>", methods=["POST"], endpoint="delete_doctor")
    @login_required
    def delete_doctor_route(doctor_id):
        try:
            delete_doctor(doctor_id)
            flash("Doctor deleted successfully.", "success")
        except Error as err:
            flash(f"Database error: {err}", "error")
        return redirect(url_for("doctors"))
