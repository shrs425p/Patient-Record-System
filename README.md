# Patient Record System

A modular Flask + MySQL web application to manage patients, doctors, appointments, and medical records.

## Features

- Authentication (admin login)
- Dashboard with summary cards and upcoming appointments
- Patient management (add, list, edit, delete, profile)
- Doctor management (add, list, edit, delete)
- Appointment management (add, list, edit, delete, status)
- Medical record management (add, list, search, edit, delete)
- Shared global UI with responsive pages

## Tech Stack

- Backend: Flask 3
- Database: MySQL
- DB Connector: mysql-connector-python
- Frontend: Jinja templates, HTML, CSS, JavaScript

## Project Structure

- app.py: Flask entrypoint and module wiring
- backend: backend package
- backend/routes: route modules
- backend/services: service modules with DB operations
- backend/db.py: DB connection config
- backend/auth.py: auth helpers and login guard
- backend/models.py: domain dataclasses
- frontend: templates, CSS, JS assets
- database/schema.sql: database schema
- database/mysql_commands.txt: SQL command reference
- scripts/reseed_data.py: reset and seed script with sample data

## Prerequisites

- Python 3.10+
- MySQL Server running locally
- A MySQL user with access to create/use patient_record_system

## Installation

1. Open terminal in project folder.
2. Create and activate virtual environment (recommended).
3. Install dependencies:

pip install -r requirements.txt

## Database Setup

1. Open MySQL client.
2. Run schema file:

source database/schema.sql

If source is not supported in your MySQL shell, copy and run the SQL statements from database/schema.sql manually.

## Configure Database Connection

Database settings are read from environment variables in backend/db.py.

Supported variables:

- DB_HOST
- DB_USER
- DB_PASSWORD
- DB_NAME

Defaults (if variables are not set):

- host: localhost
- user: root
- password: shrs
- database: patient_record_system

Example (PowerShell):

$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="patient_record_system"

## Run the Application

From project root:

python app.py

Open in browser:

http://127.0.0.1:5000

Default login:

- username: admin
- password: password

## Seed / Reset Demo Data

To clear and insert fresh sample data:

python scripts/reseed_data.py

Current seed targets include 30+ rows across major sections:

- patients
- doctors
- appointments
- medical records

## Useful SQL Reference

See:

- database/mysql_commands.txt

## Architecture Overview

Request flow:

1. Browser sends request to a route in backend/routes
2. Route validates input and delegates to backend/services
3. Service executes MySQL queries through backend/db.py
4. Route renders frontend templates with response data

This keeps app.py small and presentation-friendly while business logic stays modular.

## Troubleshooting

- If python app.py fails from wrong folder, first go to project root and run again.
- If DB errors occur, verify MySQL is running and credentials match backend/db.py.
- If tables are missing, re-run database/schema.sql.

## License

For educational and demonstration use.
