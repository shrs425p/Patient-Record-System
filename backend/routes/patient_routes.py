from flask import flash, redirect, render_template, request, url_for
from mysql.connector import Error

from backend.auth import login_required
from backend.services.patient_service import (
    create_patient,
    delete_patient,
    get_patient_by_id,
    get_patient_profile_data,
    list_patients,
    update_patient,
)


def register_patient_routes(app):
    @app.route("/patients", endpoint="patients")
    @login_required
    def patients():
        patient_list = []
        try:
            patient_list = list_patients()
        except Error as err:
            flash(f"Database error: {err}", "error")

        return render_template("patients/patients.html", patients=patient_list)

    @app.route("/patients/<int:patient_id>", endpoint="view_patient")
    @login_required
    def view_patient(patient_id):
        patient = None
        records = []
        appointments = []
        try:
            patient, records, appointments = get_patient_profile_data(patient_id)
            if not patient:
                flash("Patient not found.", "error")
                return redirect(url_for("patients"))
        except Error as err:
            flash(f"Database error: {err}", "error")

        return render_template(
            "patients/patient_profile.html",
            patient=patient,
            records=records,
            appointments=appointments,
        )

    @app.route("/patients/add", methods=["GET", "POST"], endpoint="add_patient")
    @login_required
    def add_patient_route():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            age = request.form.get("age", "").strip()
            gender = request.form.get("gender", "").strip()
            phone = request.form.get("phone", "").strip()
            address = request.form.get("address", "").strip()
            description = request.form.get("description", "").strip()

            if not name or not age or not gender:
                flash("Name, age, and gender are required.", "error")
                return redirect(url_for("add_patient"))

            try:
                create_patient(name, age, gender, phone, address, description)
                flash("Patient added successfully.", "success")
                return redirect(url_for("patients"))
            except Error as err:
                flash(f"Database error: {err}", "error")

        return render_template("patients/add_patient.html")

    @app.route("/patients/edit/<int:patient_id>", methods=["GET", "POST"], endpoint="edit_patient")
    @login_required
    def edit_patient_route(patient_id):
        try:
            if request.method == "POST":
                name = request.form.get("name", "").strip()
                age_str = request.form.get("age", "").strip()
                gender = request.form.get("gender", "").strip()
                phone = request.form.get("phone", "").strip()
                address = request.form.get("address", "").strip()
                description = request.form.get("description", "").strip()

                if not name or not age_str or not gender:
                    flash("Name, age, and gender are required.", "error")
                    return redirect(url_for("edit_patient", patient_id=patient_id))

                try:
                    age = int(age_str)
                except ValueError:
                    flash("Age must be a whole number.", "error")
                    return redirect(url_for("edit_patient", patient_id=patient_id))

                update_patient(patient_id, name, age, gender, phone, address, description)
                flash("Patient updated successfully.", "success")
                return redirect(url_for("patients"))

            patient = get_patient_by_id(patient_id)
            if not patient:
                flash("Patient not found.", "error")
                return redirect(url_for("patients"))

            return render_template("patients/edit_patient.html", patient=patient)
        except Error as err:
            flash(f"Database error: {err}", "error")
            return redirect(url_for("patients"))

    @app.route("/patients/delete/<int:patient_id>", methods=["POST"], endpoint="delete_patient")
    @login_required
    def delete_patient_route(patient_id):
        try:
            delete_patient(patient_id)
            flash("Patient deleted successfully.", "success")
        except Error as err:
            flash(f"Database error: {err}", "error")
        return redirect(url_for("patients"))
