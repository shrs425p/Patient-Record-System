from dataclasses import dataclass
from typing import Optional


@dataclass
class Patient:
    id: int
    name: str
    age: int
    gender: str
    phone: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Doctor:
    id: int
    name: str
    specialty: str
    phone: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Appointment:
    id: int
    patient_id: int
    doctor_id: int
    date: str
    reason: Optional[str] = None
    status: str = "Scheduled"


@dataclass
class MedicalRecord:
    id: int
    appointment_id: int
    diagnosis: str
    prescription: Optional[str] = None
