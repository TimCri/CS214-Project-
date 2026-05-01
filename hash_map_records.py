from __future__ import annotations

'''
These imports are used only for type hints:
- Dict means a dictionary mapping keys to values
- List means a list of records
- Optional means the function may return a PatientRecord or None
'''
from typing import Dict, List, Optional

from model import PatientRecord


class HashMapRecords:
    '''
    This class stores patient records using a Python dictionary.
    In this project, the dictionary represents a hash map:
    - key   -> record.id
    - value -> PatientRecord
    '''
    def __init__(self) -> None:
        # The dictionary acts as a hash map.
        # Record ID is the key, and the full patient record is the value.
        self.records: Dict[int, PatientRecord] = {}

    def insert_record(self, record: PatientRecord) -> None:
        # Insert/update by key.
        self.records[record.id] = record

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        # Hash maps are fast for lookup on average because they use hashed keys.
        return self.records.get(record_id)

    def delete_record(self, record_id: int) -> bool:
        # Delete a record by its ID.
        # First, check whether the key exists.
        # This avoids trying to delete a missing key, which would raise an error.
        if record_id in self.records:
            # Remove the key-value pair from the dictionary.
            del self.records[record_id]
            # Return True to signal that a record was found and removed.
            return True
        # Return False when the requested ID was not found.
        # This gives the caller a clear success/failure result.
        return False

    def traverse_records(self) -> List[PatientRecord]:
        # Traversal returns all stored values.
        # Dictionary order is insertion order in modern Python.
        return list(self.records.values())
