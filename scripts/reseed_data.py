import random
from datetime import date, timedelta
from pathlib import Path
import sys

import mysql.connector

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.db import DB_CONFIG

random.seed(42)


def build_patients(count=40):
    first_names = [
        "Aarav", "Vivaan", "Aditya", "Krishna", "Arjun", "Ishaan", "Rohan", "Kunal", "Siddharth", "Manav",
        "Ananya", "Diya", "Aisha", "Priya", "Sneha", "Kavya", "Riya", "Meera", "Pooja", "Nisha",
    ]
    last_names = [
        "Sharma", "Verma", "Gupta", "Patel", "Nair", "Iyer", "Reddy", "Mehta", "Bose", "Singh",
        "Khan", "Das", "Kulkarni", "Joshi", "Chopra", "Yadav", "Mishra", "Menon", "Ghosh", "Batra",
    ]
    cities = [
        "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow",
        "Indore", "Bhopal", "Kochi", "Nagpur", "Surat", "Patna", "Noida", "Chandigarh", "Guwahati", "Mysuru",
    ]
    notes = [
        "Diabetic patient under regular monitoring",
        "History of mild hypertension",
        "Seasonal allergies reported",
        "Undergoing physiotherapy follow-up",
        "No major prior medical history",
        "Requires periodic thyroid profile tests",
        "Observed vitamin D deficiency",
        "Occasional migraine episodes",
    ]

    patients = []
    for i in range(count):
        first = first_names[i % len(first_names)]
        last = last_names[(i * 3) % len(last_names)]
        name = f"{first} {last}"
        age = random.randint(19, 76)
        gender = ["Male", "Female", "Other"][i % 3]
        phone = f"9{random.randint(100000000, 999999999)}"
        address = f"{random.randint(11, 499)}, Sector {random.randint(1, 24)}, {cities[i % len(cities)]}"
        description = notes[i % len(notes)]
        patients.append((name, age, gender, phone, address, description))
    return patients


def build_doctors(count=32):
    doctor_first = [
        "Amit", "Neha", "Rajesh", "Sunita", "Vikram", "Pallavi", "Suresh", "Anita", "Deepak", "Ritu",
        "Harish", "Swati", "Nitin", "Bhavna", "Prakash", "Shalini", "Ajay", "Priti", "Rakesh", "Madhuri",
    ]
    doctor_last = [
        "Rao", "Kapoor", "Malhotra", "Saxena", "Trivedi", "Bhandari", "Chatterjee", "Agarwal", "Deshmukh", "Tandon",
        "Sethi", "Pillai", "Basu", "Dubey", "Bhatt", "Sarin", "Pandey", "Soman", "Lal", "Arora",
    ]
    specialties = [
        "General Medicine", "Cardiology", "Neurology", "Orthopedics", "Dermatology", "Pediatrics", "Gynecology",
        "ENT", "Ophthalmology", "Psychiatry", "Endocrinology", "Gastroenterology",
    ]

    doctors = []
    for i in range(count):
        first = doctor_first[i % len(doctor_first)]
        last = doctor_last[(i * 2) % len(doctor_last)]
        name = f"Dr. {first} {last}"
        specialty = specialties[i % len(specialties)]
        phone = f"98{random.randint(10000000, 99999999)}"
        email = f"{first.lower()}.{last.lower()}{i+1}@clinic.in"
        description = f"Consultant in {specialty} with {6 + (i % 12)} years of clinical experience."
        doctors.append((name, specialty, phone, email, description))
    return doctors


def build_appointments(count=60, patient_count=40, doctor_count=32):
    reasons = [
        "Routine health checkup",
        "Fever and body ache",
        "Follow-up consultation",
        "Blood pressure review",
        "Thyroid medication adjustment",
        "Skin allergy flare-up",
        "Headache and dizziness",
        "Joint pain evaluation",
        "Stomach discomfort",
        "Diabetes review",
        "Eye irritation and dryness",
        "ENT infection symptoms",
    ]

    start = date.today() - timedelta(days=25)
    appointments = []
    for i in range(count):
        patient_id = random.randint(1, patient_count)
        doctor_id = random.randint(1, doctor_count)
        appt_date = start + timedelta(days=random.randint(0, 70))
        reason = reasons[i % len(reasons)]
        if i < 40:
            status = "Completed"
        elif i < 52:
            status = "Scheduled"
        else:
            status = "Cancelled"
        appointments.append((patient_id, doctor_id, appt_date, reason, status))
    return appointments


def build_records(completed_appointment_ids, max_records=45):
    diagnoses = [
        "Viral fever",
        "Migraine",
        "Mild gastritis",
        "Seasonal allergic rhinitis",
        "Type 2 diabetes mellitus",
        "Primary hypertension",
        "Lumbar strain",
        "Hypothyroidism",
        "Acute sinusitis",
        "Conjunctivitis",
    ]
    prescriptions = [
        "Paracetamol 650mg twice daily for 3 days",
        "Sumatriptan 50mg as needed, max 2 per day",
        "Pantoprazole 40mg before breakfast for 7 days",
        "Levocetirizine 5mg at night for 5 days",
        "Metformin 500mg twice daily after meals",
        "Telmisartan 40mg once daily",
        "Diclofenac gel local application twice daily",
        "Levothyroxine 50mcg every morning",
        "Steam inhalation and Amoxiclav for 5 days",
        "Lubricating eye drops four times daily",
    ]

    records = []
    for idx, appt_id in enumerate(completed_appointment_ids[:max_records]):
        diagnosis = diagnoses[idx % len(diagnoses)]
        prescription = prescriptions[idx % len(prescriptions)]
        records.append((appt_id, diagnosis, prescription))
    return records


def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        cur.execute("DELETE FROM medical_record")
        cur.execute("DELETE FROM appointment")
        cur.execute("DELETE FROM patient")
        cur.execute("DELETE FROM doctor")

        cur.execute("ALTER TABLE medical_record AUTO_INCREMENT = 1")
        cur.execute("ALTER TABLE appointment AUTO_INCREMENT = 1")
        cur.execute("ALTER TABLE patient AUTO_INCREMENT = 1")
        cur.execute("ALTER TABLE doctor AUTO_INCREMENT = 1")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1")

        patients = build_patients(40)
        doctors = build_doctors(32)
        appointments = build_appointments(60, 40, 32)

        cur.executemany(
            """
            INSERT INTO patient (name, age, gender, phone, address, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            patients,
        )

        cur.executemany(
            """
            INSERT INTO doctor (name, specialty, phone, email, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            doctors,
        )

        cur.executemany(
            """
            INSERT INTO appointment (patient_id, doctor_id, date, reason, status)
            VALUES (%s, %s, %s, %s, %s)
            """,
            appointments,
        )

        cur.execute("SELECT id FROM appointment WHERE status = 'Completed' ORDER BY id ASC")
        completed_ids = [row["id"] for row in cur.fetchall()]

        records = build_records(completed_ids, 45)
        cur.executemany(
            """
            INSERT INTO medical_record (appointment_id, diagnosis, prescription)
            VALUES (%s, %s, %s)
            """,
            records,
        )

        conn.commit()

        cur.execute("SELECT COUNT(*) AS c FROM patient")
        patients_count = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM doctor")
        doctors_count = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM appointment")
        appointments_count = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM medical_record")
        records_count = cur.fetchone()["c"]

        print("Reseed complete.")
        print(f"Patients: {patients_count}")
        print(f"Doctors: {doctors_count}")
        print(f"Appointments: {appointments_count}")
        print(f"Medical Records: {records_count}")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
