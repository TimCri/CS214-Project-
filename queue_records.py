from __future__ import annotations

'''
deque is used because it supports efficient queue-style insertions
and removals from the ends.
'''
from collections import deque

'''
These typing imports make the queue code easier to understand:
- Deque: used for internal queue storage
- List: used when returning traversal results
- Optional: used when search may return a record or None
'''
from typing import Deque, List, Optional

from model import PatientRecord


class QueueRecords:
    def __init__(self) -> None:
        # deque is used as the underlying queue storage.
        self.records: Deque[PatientRecord] = deque()

    def insert_record(self, record: PatientRecord) -> None:
        # Insert adds a patient to the back of the queue.
        self.records.append(record)

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        # Queues do not support direct lookup by record ID.
        # We scan the queue from front to back until a match is found.
        for record in self.records:
            if record.id == record_id:
                return record
        return None

    def delete_record(self, record_id: int) -> bool:
        # Queue deletion by arbitrary ID is not a natural queue operation.
        # To support the project requirement, rebuild the queue while skipping
        # the first matching record.
        buffer: Deque[PatientRecord] = deque()
        deleted = False

        while self.records:
            record = self.records.popleft()

            if not deleted and record.id == record_id:
                deleted = True
                continue

            buffer.append(record)

        self.records = buffer
        return deleted

    def traverse_records(self) -> List[PatientRecord]:
        # Return all records in front-to-back queue order.
        return list(self.records)
