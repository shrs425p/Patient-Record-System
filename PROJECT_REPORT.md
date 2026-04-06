# Project Report

## Project Title
Patient Record System

## Group Members
| Roll No. | Full Name |
|---|---|
| 53 | Shreyas Pawar |

## Technologies Used
- Language: Python 3
- Database: MySQL
- Framework: Flask 3
- Frontend: HTML5, CSS3, JavaScript, Jinja templates

## Technologies, Libraries and Modules
### Third-party libraries
- Flask==3.0.3
- mysql-connector-python==9.0.0
- Werkzeug security utilities

### Python standard library modules
- os
- pathlib
- functools
- dataclasses
- typing
- datetime
- random
- sys

## Project Description
The Patient Record System is a modular web application used to manage hospital data for patients, doctors, appointments, and medical records in one place.
It provides secure login, dashboard insights, and complete CRUD operations for all major entities.
The system uses a MySQL-backed architecture with route-service separation for maintainability and clean code structure.

## ER Diagram
See: database/ER_DIAGRAM.md

## Conclusion
This project helped us apply DBMS concepts such as relational schema design, primary and foreign keys, one-to-many and one-to-one relationships, and referential integrity.
We successfully integrated Flask with MySQL to build a full-stack system with authentication and real-world CRUD workflows.
The final outcome is a practical and scalable patient management solution suitable for academic demonstration.

## Functions Used
- initialize_auth_storage
- authenticate_user
- change_user_password
- get_db_connection
- register_auth_routes
- register_core_routes
- register_patient_routes
- register_doctor_routes
- register_appointment_routes
- register_record_routes
- get_dashboard_data
- get_sidebar_stats
- create_patient, update_patient, delete_patient
- create_doctor, update_doctor, delete_doctor
- create_appointment, update_appointment, delete_appointment
- create_record, update_record, delete_record
- main (reseed script)

## Code Snippets
Sample Flask app setup and route registration:

```python
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

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = Flask(
	__name__,
	template_folder=str(FRONTEND_DIR),
	static_folder=str(FRONTEND_DIR),
)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "patient-record-secret")

initialize_auth_storage()

register_auth_routes(app)
register_core_routes(app)
register_patient_routes(app)
register_doctor_routes(app)
register_appointment_routes(app)
register_record_routes(app)

if __name__ == "__main__":
	app.run(debug=True)
```

## Results and Screenshots
Add your screenshots in the placeholders below.

### Screenshot 1: Login Page
[Insert screenshot here]

### Screenshot 2: Dashboard
[Insert screenshot here]

### Screenshot 3: Patients Module
[Insert screenshot here]

### Screenshot 4: Doctors Module
[Insert screenshot here]

### Screenshot 5: Appointments Module
[Insert screenshot here]

### Screenshot 6: Medical Records Module
[Insert screenshot here]
