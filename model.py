from __future__ import annotations

from dataclasses import dataclass
'

'
@dataclass
class PatientRecord:
    id: int
    name: str
    age: int
    gender: str
    medical_condition: str
    hospital: str
    insurance_provider: str
    billing_amount: float
    admission_type: str
