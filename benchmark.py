from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List

from model import PatientRecord

# This object stores the final benchmark output for one test run.
@dataclass(frozen=True)
class BenchmarkResult:
    structure_name: str
    operation_name: str
    record_count: int
    runs: int
    average_seconds: float
    time_complexity: str

# Time complexity labels shown to the user.
# These are theoretical averages/worst-case summaries for the chosen operation.
OPERATION_COMPLEXITIES: Dict[str, Dict[str, str]] = {
    "Dynamic Array": {
        "insert": "O(1) amortized",
        "search": "O(n)",
        "delete": "O(n)",
        "traverse": "O(n)",
    },
    "Linked List": {
        "insert": "O(1)",
        "search": "O(n)",
        "delete": "O(n)",
        "traverse": "O(n)",
    },
    "Queue": {
        "insert": "O(1)",
        "search": "O(n)",
        "delete": "O(n)",
        "traverse": "O(n)",
    },
    "Hash Map": {
        "insert": "O(1) average",
        "search": "O(1) average",
        "delete": "O(1) average",
        "traverse": "O(n)",
    },
}


def format_seconds(seconds: float) -> str:
    return f"{seconds:.8f} sec"


def build_structure(structure: Any, records: Iterable[PatientRecord]) -> Any:
    # Many benchmarks need a fully populated structure before timing an operation.
    # This helper avoids repeating the same insert loop everywhere.
    for record in records:
        structure.insert_record(record)
    return structure


def benchmark_insert(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    timings: List[float] = []

    for _ in range(runs):
        structure = structure_class()
        # Measure only the insert phase.
        start = time.perf_counter()
        for record in records:
            structure.insert_record(record)
        end = time.perf_counter()
        timings.append(end - start)
    # We use the average to smooth out small runtime fluctuations.
    return statistics.mean(timings)


def benchmark_search(
    structure_class: Any,
    records: List[PatientRecord],
    search_id: int,
    runs: int = 5,
) -> float:
    timings: List[float] = []

    for _ in range(runs):
        # Search should be timed on a structure that already contains data.
        structure = build_structure(structure_class(), records)
        start = time.perf_counter()
        structure.search_record(search_id)
        end = time.perf_counter()
        timings.append(end - start)

    return statistics.mean(timings)


def benchmark_delete(
    structure_class: Any,
    records: List[PatientRecord],
    delete_id: int,
    runs: int = 5,
) -> float:
    timings: List[float] = []

    for _ in range(runs):
        # Delete is measured on a fresh copy each run so one deletion does not affect the next run.
        structure = build_structure(structure_class(), records)
        start = time.perf_counter()
        structure.delete_record(delete_id)
        end = time.perf_counter()
        timings.append(end - start)

    return statistics.mean(timings)


def benchmark_traverse(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    timings: List[float] = []

    for _ in range(runs):
        structure = build_structure(structure_class(), records)
        start = time.perf_counter()
        structure.traverse_records()
        end = time.perf_counter()
        timings.append(end - start)

    return statistics.mean(timings)


def run_selected_benchmark(
    structure_name: str,
    structure_class: Any,
    operation_name: str,
    records: List[PatientRecord],
    runs: int = 5,
) -> BenchmarkResult:
    if not records:
        raise ValueError("At least one record is required for benchmarking.")
    # Each operation maps to the benchmark function that knows how to time it.
    # We choose one based on the user's menu selection.
    operations: Dict[str, Callable[[], float]] = {
        "insert": lambda: benchmark_insert(structure_class, records, runs),
        "search": lambda: benchmark_search(structure_class, records, records[len(records) // 2].id, runs),
        "delete": lambda: benchmark_delete(structure_class, records, records[-1].id, runs),
        "traverse": lambda: benchmark_traverse(structure_class, records, runs),
    }

    if operation_name not in operations:
        raise ValueError(f"Unsupported operation: {operation_name}")

    average_seconds = operations[operation_name]()
    complexity = OPERATION_COMPLEXITIES[structure_name][operation_name]

    return BenchmarkResult(
        structure_name=structure_name,
        operation_name=operation_name,
        record_count=len(records),
        runs=runs,
        average_seconds=average_seconds,
        time_complexity=complexity,
    )
