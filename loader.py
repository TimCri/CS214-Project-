from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from model import PatientRecord


def load_patient_records(csv_file_path: str | Path, limit: int | None = None) -> List[PatientRecord]:
    csv_path = Path(csv_file_path).expanduser().resolve()

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    records: List[PatientRecord] = []

    with csv_path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for index, row in enumerate(reader, start=1):
            if limit is not None and len(records) >= limit:
                break

            try:
                records.append(
                    PatientRecord(
                        id=index,
                        name=str(row["Name"]).strip(),
                        age=int(row["Age"]),
                        gender=str(row["Gender"]).strip(),
                        medical_condition=str(row["Medical Condition"]).strip(),
                        hospital=str(row["Hospital"]).strip(),
                        insurance_provider=str(row["Insurance Provider"]).strip(),
                        billing_amount=float(row["Billing Amount"]),
                        admission_type=str(row["Admission Type"]).strip(),
                    )
                )
            except (KeyError, ValueError, TypeError) as error:
                print(f"Skipping invalid row {index}: {error}")

    return records