CREATE DATABASE IF NOT EXISTS patient_record_system;
USE patient_record_system;

CREATE TABLE IF NOT EXISTS patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255),
    description TEXT
);

CREATE TABLE IF NOT EXISTS doctor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    description TEXT
);

CREATE TABLE IF NOT EXISTS appointment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    date DATE NOT NULL,
    reason VARCHAR(255),
    status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    CONSTRAINT fk_appointment_patient
        FOREIGN KEY (patient_id) REFERENCES patient(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_appointment_doctor
        FOREIGN KEY (doctor_id) REFERENCES doctor(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS medical_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL UNIQUE,
    diagnosis VARCHAR(255) NOT NULL,
    prescription TEXT,
    CONSTRAINT fk_record_appointment
        FOREIGN KEY (appointment_id) REFERENCES appointment(id)
        ON DELETE CASCADE
);
