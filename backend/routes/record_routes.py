from flask import flash, redirect, render_template, request, url_for
from mysql.connector import Error

from backend.auth import login_required
from backend.services.record_service import (
    create_record,
    delete_record,
    get_record_by_id,
    list_appointments_for_record_select,
    list_records,
    update_record,
)


def register_record_routes(app):
    @app.route("/records", methods=["GET"], endpoint="records")
    @login_required
    def records():
        search = request.args.get("search", "").strip()
        record_list = []
        appointment_list = []

        try:
            record_list, appointment_list = list_records(search)
        except Error as err:
            flash(f"Database error: {err}", "error")

        return render_template(
            "records/records.html",
            records=record_list,
            search=search,
            appointments=appointment_list,
        )

    @app.route("/records/add", methods=["POST"], endpoint="add_record")
    @login_required
    def add_record_route():
        appointment_id = request.form.get("appointment_id", "").strip()
        diagnosis = request.form.get("diagnosis", "").strip()
        prescription = request.form.get("prescription", "").strip()

        if not appointment_id or not diagnosis:
            flash("Appointment and diagnosis are required.", "error")
            return redirect(url_for("records"))

        try:
            create_record(appointment_id, diagnosis, prescription)
            flash("Medical record added successfully.", "success")
        except Error as err:
            flash(f"Database error: {err}", "error")

        return redirect(url_for("records"))

    @app.route("/records/edit/<int:record_id>", methods=["GET", "POST"], endpoint="edit_record")
    @login_required
    def edit_record_route(record_id):
        try:
            if request.method == "POST":
                appointment_id = request.form.get("appointment_id")
                diagnosis = request.form.get("diagnosis", "").strip()
                prescription = request.form.get("prescription", "").strip()

                if not appointment_id or not diagnosis:
                    flash("Appointment and Diagnosis are required.", "error")
                    return redirect(url_for("edit_record", record_id=record_id))

                update_record(record_id, appointment_id, diagnosis, prescription)
                flash("Medical Record updated successfully.", "success")
                return redirect(url_for("records"))

            record = get_record_by_id(record_id)
            if not record:
                flash("Medical Record not found.", "error")
                return redirect(url_for("records"))

            appointment_list = list_appointments_for_record_select()
            return render_template(
                "records/edit_record.html",
                record=record,
                appointments=appointment_list,
            )
        except Error as err:
            flash(f"Database error: {err}", "error")
            return redirect(url_for("records"))

    @app.route("/records/delete/<int:record_id>", methods=["POST"], endpoint="delete_record")
    @login_required
    def delete_record_route(record_id):
        try:
            delete_record(record_id)
            flash("Medical record deleted successfully.", "success")
        except Error as err:
            flash(f"Database error: {err}", "error")
        return redirect(url_for("records"))
