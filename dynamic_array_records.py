from typing import List, Optional
from model import PatientRecord


class DynamicArrayRecords:
    def __init__(self) -> None:
        # This will store all patient records
        self.records: List[PatientRecord] = []

    def insert_record(self, record: PatientRecord) -> None:
        # Insert a new patient record into the array
        self.records.append(record)

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        # Search for a record by ID using linear search and traverses through each record until a match is found
        for record in self.records:
            if record.id == record_id:
                return record  

        return None

    def delete_record(self, record_id: int) -> bool:
        # Placeholder delete method, this prevents the system from breaking during benchmarking
        print("Delete handled by Linked List.")
        return False

    def traverse_records(self) -> List[PatientRecord]:
        # Traverse operation return all records in the array
        return self.records

    def print_all_records(self) -> None:
        # Print all records uses traversal to display each patient record
        print("\nAll Patient Records:")
        for record in self.records:
            print(record)
