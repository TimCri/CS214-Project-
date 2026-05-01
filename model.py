'''
This future import lets us use modern type hint behavior consistently.
It delays evaluation of type annotations until later, which helps avoid
issues with forward references and keeps typing cleaner across the project.
'''
from __future__ import annotations

'''
dataclass automatically generates common class methods for us, such as:
 __init__  -> creates the constructor
__repr__  -> gives a readable object printout
__eq__    -> allows object comparison by field values
This is useful here because PatientRecord is mostly a container for data.
'''
from dataclasses import dataclass

# A simple data container for one patient record.
# This is the shared model used by every data structure.

@dataclass
class PatientRecord:
    # A unique numeric ID assigned in loader.py.
    # We use this as the main key for searching and deleting records.
    id: int
    name: str
    age: int
    gender: str
    medical_condition: str
    hospital: str
    insurance_provider: str
    billing_amount: float
    admission_type: str
