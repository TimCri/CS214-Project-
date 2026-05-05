from __future__ import annotations

from collections import deque
from typing import Deque, List, Optional
import heapq

from model import PatientRecord


class HospitalRecords:
    def __init__(self) -> None:
        '''
        Two structures are used:

        1. deque (Queue):
           - Stores regular patients
           - First-In-First-Out (FIFO)
           - Efficient O(1) insert and remove

        2. heapq (Priority Queue):
           - Stores emergency patients
           - Patients with lower severity value are treated first
           - Efficient O(log n) insertion and removal
        '''
        self.records: Deque[PatientRecord] = deque()
        self.emergency_heap: List[tuple[int, PatientRecord]] = []

    def insert_record(self, record: PatientRecord) -> None:
        '''
        Adds a patient into the system.

        Logic:
        - If severity is high (1 or 2), treat as emergency
        - Otherwise, treat as a regular appointment
        '''
        if record.severity <= 2:
            # Push into priority queue (heap)
            # Tuple ensures sorting by severity
            heapq.heappush(self.emergency_heap, (record.severity, record))
        else:
            # Add to regular queue
            self.records.append(record)

    def treat_next_patient(self) -> Optional[PatientRecord]:
        '''
        Determines which patient should be treated next.

        Priority:
        1. Emergency patients (priority queue)
        2. Regular patients (queue)

        Returns:
        - The next patient to treat
        - None if no patients exist
        '''
        # Check emergency patients first
        if self.emergency_heap:
            return heapq.heappop(self.emergency_heap)[1]

        # If no emergencies, check regular queue
        if self.records:
            return self.records.popleft()

        # No patients available
        return None

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        '''
        Searches for a patient by ID.

        Note:
        - Queue does not support direct lookup
        - Must scan through all records
        - Also checks emergency queue
        '''
        # Search regular queue
        for record in self.records:
            if record.id == record_id:
                return record

        # Search emergency queue
        for _, record in self.emergency_heap:
            if record.id == record_id:
                return record

        return None

    def delete_record(self, record_id: int) -> bool:
        '''
        Deletes a patient by ID.

        Since queues do not support direct removal:
        - Rebuild both structures without the target record

        Returns:
        - True if deleted
        - False if not found
        '''
        deleted = False

        # Rebuild regular queue
        buffer_queue: Deque[PatientRecord] = deque()
        while self.records:
            record = self.records.popleft()

            if not deleted and record.id == record_id:
                deleted = True
                continue

            buffer_queue.append(record)

        self.records = buffer_queue

        # Rebuild emergency heap
        buffer_heap = []
        while self.emergency_heap:
            severity, record = heapq.heappop(self.emergency_heap)

            if not deleted and record.id == record_id:
                deleted = True
                continue

            buffer_heap.append((severity, record))

        # Restore heap structure
        for item in buffer_heap:
            heapq.heappush(self.emergency_heap, item)

        return deleted

    def traverse_records(self) -> List[PatientRecord]:
        '''
        Returns all patients in the system.

        Output:
        - Emergency patients first (sorted by severity)
        - Then regular patients in queue order
        '''
        emergency_sorted = [record for _, record in sorted(self.emergency_heap)]
        regular_list = list(self.records)

        return emergency_sorted + regular_list
