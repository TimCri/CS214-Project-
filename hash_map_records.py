from __future__ import annotations

from typing import Dict, List, Optional

from model import PatientRecord


class HashMapRecords:
    def __init__(self) -> None:
        self.records: Dict[int, PatientRecord] = {}

    def insert_record(self, record: PatientRecord) -> None:
        self.records[record.id] = record

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        return self.records.get(record_id)

    def delete_record(self, record_id: int) -> bool:
        if record_id in self.records:
            del self.records[record_id]
            return True
        return False

    def traverse_records(self) -> List[PatientRecord]:
        return list(self.records.values())