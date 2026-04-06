# ER Diagram - Patient Record System

This ERD is generated from the current MySQL schema in database/schema.sql.

```mermaid
erDiagram
    USERS {
        INT id PK
        VARCHAR username UK "NOT NULL"
        VARCHAR password_hash "NOT NULL"
        TIMESTAMP created_at "DEFAULT CURRENT_TIMESTAMP"
    }

    PATIENT {
        INT id PK
        VARCHAR name "NOT NULL"
        INT age "NOT NULL"
        VARCHAR gender "NOT NULL"
        VARCHAR phone
        VARCHAR address
        TEXT description
    }

    DOCTOR {
        INT id PK
        VARCHAR name "NOT NULL"
        VARCHAR specialty "NOT NULL"
        VARCHAR phone
        VARCHAR email
        TEXT description
    }

    APPOINTMENT {
        INT id PK
        INT patient_id FK "NOT NULL"
        INT doctor_id FK "NOT NULL"
        DATE date "NOT NULL"
        VARCHAR reason
        ENUM status "Pending | Completed | Cancelled"
    }

    MEDICAL_RECORD {
        INT id PK
        INT appointment_id FK, UK "NOT NULL, UNIQUE"
        VARCHAR diagnosis "NOT NULL"
        TEXT prescription
    }

    PATIENT ||--o{ APPOINTMENT : books
    DOCTOR ||--o{ APPOINTMENT : handles
    APPOINTMENT ||--o| MEDICAL_RECORD : produces
```

## Cardinality Summary
- PATIENT (1) to APPOINTMENT (0..N)
- DOCTOR (1) to APPOINTMENT (0..N)
- APPOINTMENT (1) to MEDICAL_RECORD (0..1)
- USERS is currently independent (no FK relation in schema)

## Key Integrity Rules
- APPOINTMENT.patient_id references PATIENT.id with ON DELETE CASCADE
- APPOINTMENT.doctor_id references DOCTOR.id with ON DELETE CASCADE
- MEDICAL_RECORD.appointment_id references APPOINTMENT.id with ON DELETE CASCADE
- MEDICAL_RECORD.appointment_id is UNIQUE, enforcing at most one medical record per appointment
- USERS.username is UNIQUE

## Business Meaning
- If a patient is deleted, all linked appointments and their medical records are deleted automatically
- If a doctor is deleted, all linked appointments and their medical records are deleted automatically
- A medical record cannot exist without an appointment

## Validation Checklist
- All PKs are surrogate integer keys (AUTO_INCREMENT)
- All FK columns are NOT NULL where relationships are mandatory
- One-to-one behavior is correctly enforced through UNIQUE on MEDICAL_RECORD.appointment_id
- Status lifecycle for appointment is restricted by ENUM values
