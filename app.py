from flask import Flask

from backend.routes.appointment_routes import register_appointment_routes
from backend.routes.auth_routes import register_auth_routes
from backend.routes.core_routes import register_core_routes
from backend.routes.doctor_routes import register_doctor_routes
from backend.routes.patient_routes import register_patient_routes
from backend.routes.record_routes import register_record_routes
from backend.services.sidebar_service import get_sidebar_stats

app = Flask(__name__, template_folder="frontend", static_folder="frontend")
app.secret_key = "patient-record-secret"


@app.context_processor
def inject_sidebar_stats():
    try:
        return get_sidebar_stats()
    except Exception as error:
        print(f"Error in context processor: {error}")
        return {"patient_count": 0, "appointment_today_count": 0}


register_auth_routes(app)
register_core_routes(app)
register_patient_routes(app)
register_doctor_routes(app)
register_appointment_routes(app)
register_record_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
