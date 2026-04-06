from flask import flash, redirect, render_template, request, url_for
from mysql.connector import Error

from backend.auth import login_required
from backend.services.appointment_service import (
    create_appointment,
    delete_appointment,
    get_appointment_by_id,
    list_appointments,
    list_doctors_for_select,
    list_patients_for_select,
    update_appointment,
)


def register_appointment_routes(app):
    @app.route("/appointments", endpoint="appointments")
    @login_required
    def appointments():
        appointment_list = []
        try:
            appointment_list = list_appointments()
        except Error as err:
            flash(f"Database error: {err}", "error")

        return render_template("appointments/appointments.html", appointments=appointment_list)

    @app.route("/appointments/add", methods=["GET", "POST"], endpoint="add_appointment")
    @login_required
    def add_appointment_route():
        patient_list = []
        doctor_list = []

        try:
            patient_list = list_patients_for_select()
            doctor_list = list_doctors_for_select()
        except Error as err:
            flash(f"Database error: {err}", "error")

        if request.method == "POST":
            patient_id = request.form.get("patient_id", "").strip()
            doctor_id = request.form.get("doctor_id", "").strip()
            date_value = request.form.get("date", "").strip()
            reason = request.form.get("reason", "").strip()
            status = request.form.get("status", "Pending").strip()

            if not patient_id or not doctor_id or not date_value:
                flash("Patient, doctor, and date are required.", "error")
                return redirect(url_for("add_appointment"))

            try:
                create_appointment(patient_id, doctor_id, date_value, reason, status)
                flash("Appointment booked successfully.", "success")
                return redirect(url_for("appointments"))
            except Error as err:
                flash(f"Database error: {err}", "error")

        return render_template(
            "appointments/add_appointment.html",
            patients=patient_list,
            doctors=doctor_list,
        )

    @app.route("/appointments/edit/<int:appointment_id>", methods=["GET", "POST"], endpoint="edit_appointment")
    @login_required
    def edit_appointment_route(appointment_id):
        try:
            if request.method == "POST":
                patient_id = request.form.get("patient_id")
                doctor_id = request.form.get("doctor_id")
                date_value = request.form.get("date")
                reason = request.form.get("reason", "").strip()
                new_status = request.form.get("status", "Pending")

                if not patient_id or not doctor_id or not date_value:
                    flash("Patient, Doctor, and Date are required.", "error")
                    return redirect(url_for("edit_appointment", appointment_id=appointment_id))

                if new_status == "Cancelled":
                    current = get_appointment_by_id(appointment_id)
                    current_status = current.get("raw_status") if current else None
                    if current_status == "Pending":
                        current_status = "Scheduled"
                    if current and current_status not in {"Scheduled", "Pending"}:
                        flash(
                            f"Cannot cancel an appointment that is already '{current['status']}'. Only Pending appointments can be cancelled.",
                            "error",
                        )
                        return redirect(url_for("edit_appointment", appointment_id=appointment_id))

                update_appointment(appointment_id, patient_id, doctor_id, date_value, reason, new_status)
                flash("Appointment updated successfully.", "success")
                return redirect(url_for("appointments"))

            appointment = get_appointment_by_id(appointment_id)
            if not appointment:
                flash("Appointment not found.", "error")
                return redirect(url_for("appointments"))

            patient_list = list_patients_for_select()
            doctor_list = list_doctors_for_select()

            return render_template(
                "appointments/edit_appointment.html",
                appointment=appointment,
                patients=patient_list,
                doctors=doctor_list,
            )
        except Error as err:
            flash(f"Database error: {err}", "error")
            return redirect(url_for("appointments"))

    @app.route("/appointments/delete/<int:appointment_id>", methods=["POST"], endpoint="delete_appointment")
    @login_required
    def delete_appointment_route(appointment_id):
        try:
            delete_appointment(appointment_id)
            flash("Appointment deleted successfully.", "success")
        except Error as err:
            flash(f"Database error: {err}", "error")
        return redirect(url_for("appointments"))
