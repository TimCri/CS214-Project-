from __future__ import annotations

'''
statistics is used to calculate the average runtime across multiple test runs.
Running the same benchmark several times helps reduce noise from tiny timing variations.
'''
import statistics

'''
time provides the high-resolution timer used for benchmarking.
perf_counter() is preferred for timing short operations because it is precise.
'''
import time

'''
dataclass automatically creates useful methods for simple data-holder classes.
Here it is used to make BenchmarkResult cleaner and easier to work with.
'''
from dataclasses import dataclass

'''
These typing imports make the purpose of variables and parameters clearer:
- Any: used where different structure classes/instances may be passed in
- Callable: used for mapping an operation name to a function we can call
- Dict: used for dictionaries such as the complexity lookup table
- Iterable: used for any collection we can loop over
- List: used for ordered collections such as timings and records
'''
from typing import Any, Callable, Dict, Iterable, List

from model import PatientRecord

'''
This dataclass represents the final output of one benchmark selection.
It bundles together everything the main program needs to display:
- which data structure was tested
- which operation was benchmarked
- how many records were used
- how many runs were averaged
- the measured average runtime
 - the theoretical time complexity

frozen=True makes instances immutable after creation.
That is helpful here because benchmark results should behave like
fixed report data, not something that gets changed later by mistake.
'''
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
    # Convert the raw timing value into a consistent string format for display.
    return f"{seconds:.8f} sec"


def build_structure(structure: Any, records: Iterable[PatientRecord]) -> Any:
    # Many benchmarks need a fully populated structure before timing an operation.
    # This helper avoids repeating the same insert loop everywhere.
    for record in records:
        structure.insert_record(record)
    return structure


def benchmark_insert(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    # This function measures the time required to insert all selected records
    # into a fresh instance of the chosen data structure.
    timings: List[float] = []

    for _ in range(runs):
        # Create a brand-new empty structure for each run.
        structure = structure_class()
        # Start timing immediately before the inserts begin.
        start = time.perf_counter()
        for record in records:
            structure.insert_record(record)
        # Stop timing right after the last insert.
        end = time.perf_counter()
        # Store the elapsed time for this run.
        timings.append(end - start)
    # We use the average to smooth out small runtime fluctuations.
    return statistics.mean(timings)


def benchmark_search(
    structure_class: Any,
    records: List[PatientRecord],
    search_id: int,
    runs: int = 5,
) -> float:
     # This function measures how long it takes to search for one record ID.
    timings: List[float] = []

    for _ in range(runs):
        # Search should be timed on a structure that already contains data.
        structure = build_structure(structure_class(), records)
        # Time only the search operation itself, not the setup.
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
    # This function measures how long it takes to delete one record ID.
    timings: List[float] = []

    for _ in range(runs):
        # Delete is measured on a fresh copy each run so one deletion does not affect the next run.
        structure = build_structure(structure_class(), records)
        # Time only the delete operation itself.
        start = time.perf_counter()
        structure.delete_record(delete_id)
        end = time.perf_counter()
        timings.append(end - start)

    return statistics.mean(timings)


def benchmark_traverse(structure_class: Any, records: List[PatientRecord], runs: int = 5) -> float:
    # This function measures how long it takes to traverse all records
    # already stored in the structure.
    timings: List[float] = []

    for _ in range(runs):
        structure = build_structure(structure_class(), records)
        # Time only the traversal step.
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
    # This is the main dispatcher for the benchmark module.
    # It receives the user's selections from main.py and routes them
    # to the correct timing function.
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
    # Reject unsupported operation names before continuing.
    if operation_name not in operations:
        raise ValueError(f"Unsupported operation: {operation_name}")
    # Run the chosen benchmark and get the measured average time.
    average_seconds = operations[operation_name]()
    # Look up the matching theoretical complexity label for display.
    complexity = OPERATION_COMPLEXITIES[structure_name][operation_name]

    # Package all details into one immutable result object.
    # main.py will print this nicely for the user.
    return BenchmarkResult(
        structure_name=structure_name,
        operation_name=operation_name,
        record_count=len(records),
        runs=runs,
        average_seconds=average_seconds,
        time_complexity=complexity,
    )
