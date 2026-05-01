from __future__ import annotations

from typing import Dict, List, Optional

from model import PatientRecord


class HashMapRecords:
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
        if record_id in self.records:
            del self.records[record_id]
            return True
        return False

    def traverse_records(self) -> List[PatientRecord]:
        # Traversal returns all stored values.
        # Dictionary order is insertion order in modern Python.
        return list(self.records.values())
