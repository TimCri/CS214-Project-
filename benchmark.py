from __future__ import annotations

import statistics
import time
from typing import Any, Iterable, List

from model import PatientRecord


def build_structure(structure: Any, records: Iterable[PatientRecord]) -> Any:
    for record in records:
        structure.insert_record(record)
    return structure


def benchmark_insert(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    timings: List[float] = []

    for _ in range(runs):
        structure = structure_class()
        start = time.perf_counter()
        for record in records:
            structure.insert_record(record)
        end = time.perf_counter()
        timings.append(end - start)

    return statistics.mean(timings)


def benchmark_search(
    structure_class: Any,
    records: List[PatientRecord],
    search_id: int,
    runs: int = 5,
) -> float:
    timings: List[float] = []

    for _ in range(runs):
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


def format_seconds(seconds: float) -> str:
    return f"{seconds:.8f} sec"