from __future__ import annotations
from typing import Optional
from model import PatientRecord


class Node:
    def __init__(self, record: PatientRecord):
        self.record = record
        self.next: Optional[Node] = None


class LinkedListRecords:
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def insert_record(self, record: PatientRecord) -> None:
        new_node = Node(record)
        new_node.next = self.head
        self.head = new_node

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        Start at head
        While current is not null:
            If record ID matches → return
            Move to next node
        current = self.head

        while current is not None:
            if current.record.id == record_id:
                return current.record
            current = current.next

        return None

    def traverse_records(self) -> list[PatientRecord]:
        current = head
        while current != null:
            display record
            move to next
        records = []
        current = self.head

        while current is not None:
            records.append(current.record)
            current = current.next

        return records


    def print_all_records(self) -> None:
        print("\nAll Patient Records:")
        current = self.head

        while current is not None:
            print(current.record)
            current = current.next


    
    def delete_record(self, record_id: int) -> bool:
    
        If head is empty → return false
        If head matches → move head
        Else traverse:
            find node
            link previous to next
      
        if self.head is None:
            return False

        # Case 1: delete head
        if self.head.record.id == record_id:
            self.head = self.head.next
            return True

        # Case 2: delete non-head
        current = self.head
        while current.next is not None:
            if current.next.record.id == record_id:
                current.next = current.next.next
                return True
            current = current.next

        return False
