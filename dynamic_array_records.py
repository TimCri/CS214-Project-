from __future__ import annotations

'''
These typing imports make the dynamic array code easier to understand:
- List: used for the internal array storage and traversal results
- Optional: used when search may return a record or None
'''
from typing import List, Optional

from model import PatientRecord


class DynamicArrayRecords:
    def __init__(self) -> None:
        # Python's list acts as the dynamic array in this project.
        # It grows automatically as new records are appended.
        self.records: List[PatientRecord] = []

    def insert_record(self, record: PatientRecord) -> None:
        # Insert a new patient record at the end of the array.
        self.records.append(record)

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        # Dynamic arrays do not provide direct lookup by record ID.
        # We use linear search and scan left to right until a match is found.
        for record in self.records:
            if record.id == record_id:
                return record

        return None

    def delete_record(self, record_id: int) -> bool:
        # Find the matching record by ID.
        # Once found, delete it from the array and return success.
        for index, record in enumerate(self.records):
            if record.id == record_id:
                del self.records[index]
                return True

        # Return False when no matching record exists.
        return False

    def traverse_records(self) -> List[PatientRecord]:
        # Return a copy of the array contents.
        # Returning a copy helps protect the internal storage from outside changes.
        return list(self.records)

    def print_all_records(self) -> None:
        # Print all records currently stored in the dynamic array.
        print("\nAll Patient Records:")
        for record in self.records:
            print(record)
