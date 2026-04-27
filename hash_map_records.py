# This class stores patient records in a hash-based structure.
# In Python, a dictionary is used to simulate a HashMap where:
# - the key is the patient ID
# - the value is the PatientRecord object
#
# Purpose:
# - Fast insertion by ID
# - Fast searching by ID
# - Fast deletion by ID
# - Easy traversal of all stored records
from __future__ import annotations

from typing import Dict, List, Optional

from model import PatientRecord


class HashMapRecords:
    # Initialize an empty dictionary that will hold patient records.
    def __init__(self) -> None:
        self.records: Dict[int, PatientRecord] = {}

    # Insert a patient record into the hash map.
    # The patient ID becomes the dictionary key.
    def insert_record(self, record: PatientRecord) -> None:
        self.records[record.id] = record

    # Search for a patient record by its ID.
    # Returns the PatientRecord if found, otherwise returns None.
    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        return self.records.get(record_id)

    # Delete a patient record by ID.
    # Returns True if the record was deleted, or False if the ID did not exist.
    def delete_record(self, record_id: int) -> bool:
        if record_id in self.records:
            del self.records[record_id]
            return True
        return False

    # Traverse all patient records currently stored in the hash map.
    # Returns a list of PatientRecord objects.
    def traverse_records(self) -> List[PatientRecord]:
        return list(self.records.values())
