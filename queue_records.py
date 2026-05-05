from __future__ import annotations

'''
dataclass is used to represent one queued admission entry more cleanly.
Each queue entry stores:
- the admission order number
- the patient record itself
'''
from dataclasses import dataclass

'''
deque is used because it supports efficient queue-style insertions
at the back and removals from the front.
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


@dataclass
class AdmissionQueueEntry:
    admission_order: int
    record: PatientRecord


class QueueRecords:
    def __init__(self) -> None:
        # deque stores patients in admission order.
        # admission_counter assigns a clear FIFO order as patients arrive.
        self.records: Deque[AdmissionQueueEntry] = deque()
        self.admission_counter = 0

    def insert_record(self, record: PatientRecord) -> None:
        # Each inserted patient is assigned the next admission order number.
        self.admission_counter += 1
        self.records.append(
            AdmissionQueueEntry(
                admission_order=self.admission_counter,
                record=record,
            )
        )

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        # Queues do not support direct lookup by record ID.
        # We scan from front to back in admission order.
        for entry in self.records:
            if entry.record.id == record_id:
                return entry.record

        return None

    def delete_record(self, record_id: int) -> bool:
        # Arbitrary deletion is not a natural queue operation.
        # To support the project requirement, rebuild the queue while skipping
        # the first matching patient record.
        buffer: Deque[AdmissionQueueEntry] = deque()
        deleted = False

        while self.records:
            entry = self.records.popleft()

            if not deleted and entry.record.id == record_id:
                deleted = True
                continue

            buffer.append(entry)

        self.records = buffer
        return deleted

    def traverse_records(self) -> List[PatientRecord]:
        # Return all patient records in FIFO admission order.
        return [entry.record for entry in self.records]

    def peek_next_admission(self) -> Optional[PatientRecord]:
        # Return the next patient to be processed without removing them.
        if not self.records:
            return None

        return self.records[0].record

    def process_next_admission(self) -> Optional[PatientRecord]:
        # Remove and return the next patient in FIFO admission order.
        if not self.records:
            return None

        return self.records.popleft().record

    def admission_order_snapshot(self) -> List[int]:
        # Return the current admission-order sequence for inspection or display.
        return [entry.admission_order for entry in self.records]
