from __future__ import annotations

'''
dataclass is used to define the node object more cleanly.
Each node stores one PatientRecord and a reference to the next node.
'''
from dataclasses import dataclass

'''
These typing imports make the linked list code easier to understand:
- List: used when returning all records during traversal
- Optional: used when a node reference may be missing, such as None
'''
from typing import List, Optional

from model import PatientRecord


'''
This class represents one node in the linked list.
Each node stores:
- one patient record
- a pointer to the next node
'''
@dataclass
class LinkedListNode:
    record: PatientRecord
    next: Optional["LinkedListNode"] = None


class LinkedListRecords:
    def __init__(self) -> None:
        # head points to the first node in the list.
        # tail points to the last node so insert at the end stays efficient.
        self.head: Optional[LinkedListNode] = None
        self.tail: Optional[LinkedListNode] = None

    def insert_record(self, record: PatientRecord) -> None:
        # Create a new node for the incoming patient record.
        node = LinkedListNode(record=record)

        # If the list is empty, the new node becomes both head and tail.
        if self.head is None:
            self.head = node
            self.tail = node
            return

        # Otherwise, connect the new node after the current tail,
        # then move tail forward to the new last node.
        assert self.tail is not None
        self.tail.next = node
        self.tail = node

    def search_record(self, record_id: int) -> Optional[PatientRecord]:
        # Linked lists do not support direct indexed lookup by ID,
        # so we scan node by node from the front.
        current = self.head

        while current is not None:
            if current.record.id == record_id:
                return current.record
            current = current.next

        return None

    def delete_record(self, record_id: int) -> bool:
        # Keep track of both current and previous nodes.
        # This lets us unlink the matching node when found.
        previous: Optional[LinkedListNode] = None
        current = self.head

        while current is not None:
            if current.record.id == record_id:
                # If deleting the first node, move head forward.
                if previous is None:
                    self.head = current.next
                else:
                    # Skip over the current node.
                    previous.next = current.next

                # If deleting the last node, move tail backward.
                if current == self.tail:
                    self.tail = previous

                return True

            previous = current
            current = current.next

        return False

    def traverse_records(self) -> List[PatientRecord]:
        # Walk from head to tail and collect each record.
        result: List[PatientRecord] = []
        current = self.head

        while current is not None:
            result.append(current.record)
            current = current.next

        return result
