from __future__ import annotations
'''
csv is the built-in Python module used to read comma-separated value files.
Our healthcare dataset is stored as a CSV, so this module lets us parse
each row into a dictionary using the column names as keys.
'''
import csv

'''
Path provides an object-oriented way to work with file paths.
It makes path handling safer and clearer than using raw strings alone.
'''
from pathlib import Path

'''
List is imported for return type hints so readers can clearly see
that this function returns a list of PatientRecord objects.
'''
from typing import List

'''
PatientRecord is the shared data model for one row in the dataset.
Every row we successfully read from the CSV will be converted into this class.
'''
from model import PatientRecord


def load_patient_records(csv_file_path: str | Path, limit: int | None = None) -> List[PatientRecord]:
    # Resolve the path so the program can reliably find the CSV file.
    csv_path = Path(csv_file_path).expanduser().resolve()

    # Stop immediately with a clear message if the dataset file does not exist.
    # This is better than letting the program fail later with a less helpful error.
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    # This list will store all successfully converted PatientRecord objects.
    records: List[PatientRecord] = []

    # Open the CSV file for reading.
    # - encoding="utf-8" handles standard text safely
    # - newline="" is the recommended way to read CSV files in Python
    with csv_path.open(mode="r", encoding="utf-8", newline="") as file:
        # DictReader reads each row as a dictionary.
        reader = csv.DictReader(file)
        # We assign our own sequential ID to each row.
        # That gives every record a consistent key for search/delete benchmarks.
        for index, row in enumerate(reader, start=1):
            # If the caller requested only a certain number of records,
            # stop loading once we reach that amount.
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
                # Bad rows are skipped so one malformed line does not crash the program.
                print(f"Skipping invalid row {index}: {error}")
    # Return all valid records that were successfully loaded and converted.
    return records
