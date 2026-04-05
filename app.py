from flask import Flask
from pathlib import Path
import os

from backend.auth import initialize_auth_storage
from backend.routes.appointment_routes import register_appointment_routes
from backend.routes.auth_routes import register_auth_routes
from backend.routes.core_routes import register_core_routes
from backend.routes.doctor_routes import register_doctor_routes
from backend.routes.patient_routes import register_patient_routes
from backend.routes.record_routes import register_record_routes
from backend.services.sidebar_service import get_sidebar_stats

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(
    __name__,
    template_folder=str(FRONTEND_DIR),
    static_folder=str(FRONTEND_DIR),
)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "patient-record-secret")

initialize_auth_storage()


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
    debug_mode = os.getenv("FLASK_DEBUG", "true").lower() in {"1", "true", "yes", "on"}
    app.run(debug=debug_mode)
