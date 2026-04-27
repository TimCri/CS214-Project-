from __future__ import annotations

import statistics
import time
from typing import Any, Iterable, List

from model import PatientRecord

# This helper function inserts every patient record into a newly created
# data structure instance.
#
# Purpose:
# - Prepare a data structure before running search, delete, or traverse benchmarks
# - Keep the benchmark code cleaner and reusable
def build_structure(structure: Any, records: Iterable[PatientRecord]) -> Any:
    for record in records:
        structure.insert_record(record)
    return structure

# Measure the average time needed to insert all records into an empty structure.
#
# Parameters:
# - structure_class: the class of the data structure being tested
# - records: the list of patient records to insert
# - runs: how many times the experiment should be repeated
#
# Returns:
# - the average runtime in seconds
def benchmark_insert(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    timings: List[float] = []

    for _ in range(runs):
        # Start with a fresh empty structure for each run.
        structure = structure_class()

        # Record the time just before insertion begins.
        start = time.perf_counter()

        # Insert all records one by one.
        for record in records:
            structure.insert_record(record)

        # Record the time immediately after insertion ends.
        end = time.perf_counter()

        # Store the elapsed time for this run.
        timings.append(end - start)

    # Return the average runtime across all runs.
    return statistics.mean(timings)

# Measure the average time needed to search for one record by ID.
#
# The structure is rebuilt before each run so that each benchmark starts
# from a consistent state.
def benchmark_search(
    structure_class: Any,
    records: List[PatientRecord],
    search_id: int,
    runs: int = 5,
) -> float:
    timings: List[float] = []

    for _ in range(runs):
        # Build and populate the structure before measuring search time.
        structure = build_structure(structure_class(), records)

        # Measure only the search operation.
        start = time.perf_counter()
        structure.search_record(search_id)
        end = time.perf_counter()

        timings.append(end - start)

    return statistics.mean(timings)

# Measure the average time needed to delete one record by ID.
#
# The structure is rebuilt before each run so the record always exists
# before deletion is attempted.
def benchmark_delete(
    structure_class: Any,
    records: List[PatientRecord],
    delete_id: int,
    runs: int = 5,
) -> float:
    timings: List[float] = []

    for _ in range(runs):
        # Build and populate the structure before measuring delete time.
        structure = build_structure(structure_class(), records)

        # Measure only the delete operation.
        start = time.perf_counter()
        structure.delete_record(delete_id)
        end = time.perf_counter()

        timings.append(end - start)

    return statistics.mean(timings)

# Measure the average time needed to traverse all records in the structure.
#
# Traversal means iterating through all stored patient records.
def benchmark_traverse(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    timings: List[float] = []

  for _ in range(runs):
        # Build and populate the structure before measuring traversal time.
        structure = build_structure(structure_class(), records)

        # Measure only the traversal operation.
        start = time.perf_counter()
        structure.traverse_records()
        end = time.perf_counter()

        timings.append(end - start)

    return statistics.mean(timings)

# Convert raw seconds into a formatted string for cleaner terminal output.
def format_seconds(seconds: float) -> str:
    return f"{seconds:.8f} sec"
