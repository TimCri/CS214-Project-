# This dataclass defines the simplified patient record used throughout the project.
# Each row from the CSV file is converted into one PatientRecord object.
# The fields match the project requirements:
# ID, Name, Age, Gender, Medical Condition, Hospital,
# Insurance Provider, Billing Amount, and Admission Type
from __future__ import annotations

from dataclasses import dataclass

@dataclass
class PatientRecord:
    # A unique ID generated while reading the dataset.
    id: int
    # The patient's full name from the dataset.
    name: str
    # The patient's age.
    age: int
    # The patient's gender.
    gender: str
    # The diagnosed medical condition for the patient.
    medical_condition: str
    # The hospital associated with the patient record.
    hospital: str
    # The patient's insurance company/provider.
    insurance_provider: str
    # The billing amount for the patient visit/admission.
    billing_amount: float
    # The admission type, such as Emergency, Urgent, or Elective.
    admission_type: str
