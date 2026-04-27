# This function loads patient data from the CSV file and converts each row
# into a PatientRecord object.
#
# Purpose:
# - Read the healthcare dataset from disk
# - Limit the number of records to 100 for the project requirement
# - Convert raw CSV values into the proper Python data types
# - Return a list of PatientRecord objects that can be inserted
#   into the selected data structures
from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from model import PatientRecord


def load_patient_records(csv_file_path: str | Path, limit: int = 100) -> List[PatientRecord]:
    # Convert the incoming path into a Path object, expand shortcuts such as "~",
    # and resolve it into an absolute path.
    # This makes file handling more reliable across different machines and folders.
    csv_path = Path(csv_file_path).expanduser().resolve()

    # Stop early with a clear error message if the dataset file cannot be found.
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # This list will hold all successfully created PatientRecord objects.
    records: List[PatientRecord] = []

    # Open the CSV file safely using UTF-8 encoding.
    # newline="" is recommended for CSV handling in Python.
    with csv_path.open(mode="r", encoding="utf-8", newline="") as file:
        # DictReader reads each row as a dictionary using the CSV header names.
        reader = csv.DictReader(file)

        # Start numbering records at 1 so each patient gets a unique ID.
        for index, row in enumerate(reader, start=1):
            # Stop once the requested number of records has been loaded.
            if len(records) >= limit:
                break

            try:
                # Create a PatientRecord object from the current CSV row.
                # The field names here must match the CSV column names exactly.
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
                # If a row has missing columns or bad data, skip it instead of
                # crashing the whole program.
                print(f"Skipping invalid row {index}: {error}")

    # Return the final list of patient records that were loaded successfully.
    return records
