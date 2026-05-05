from __future__ import annotations

'''
statistics is used to calculate the average runtime and memory usage
across multiple test runs.
'''
import statistics

'''
time provides the high-resolution timer used for benchmarking.
perf_counter() is preferred for timing short operations because it is precise.
'''
import time

'''
tracemalloc measures Python memory allocations during each benchmarked operation.
This lets the project report average peak memory alongside runtime.
'''
import tracemalloc

'''
dataclass automatically creates useful methods for simple data-holder classes.
Here it is used to make BenchmarkResult cleaner and easier to work with.
'''
from dataclasses import dataclass

'''
These typing imports make the purpose of variables and parameters clearer:
- Any: used where different structure classes or instances may be passed in
- Callable: used for mapping an operation name to a function we can call
- Dict: used for dictionaries such as lookup tables and summary tables
- Iterable: used for any collection we can loop through
- List: used for ordered collections such as timings and records
- Tuple: used when returning both time and memory measurements
'''
from typing import Any, Callable, Dict, Iterable, List, Tuple

from model import PatientRecord


'''
This dataclass represents the final output of one benchmark selection.
It bundles together everything the main program needs to display:
- which data structure was tested
- which operation was benchmarked
- how many records were used
- how many runs were averaged
- the measured average runtime
- the measured average peak memory usage
- the theoretical time complexity
'''
@dataclass(frozen=True)
class BenchmarkResult:
    structure_name: str
    operation_name: str
    record_count: int
    runs: int
    average_seconds: float
    average_peak_memory_bytes: int
    time_complexity: str


# These are theoretical Big-O labels.
# They are not calculated from the measured benchmark results.
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


def format_memory_size(memory_bytes: int) -> str:
    # Convert raw byte counts into a more readable unit for console output.
    units = ["B", "KB", "MB", "GB"]
    size = float(memory_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{memory_bytes} B"


def build_structure(structure: Any, records: Iterable[PatientRecord]) -> Any:
    # Many benchmarks need a fully populated structure before timing an operation.
    for record in records:
        structure.insert_record(record)

    return structure


def measure_operation(operation: Callable[[], Any]) -> Tuple[float, int]:
    # Measure both runtime and peak memory for one operation call.
    # Only the selected operation is measured, not the structure setup.
    tracemalloc.start()

    try:
        start = time.perf_counter()
        operation()
        end = time.perf_counter()
        _, peak_memory = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    return end - start, peak_memory


def run_insert_operation(structure: Any, records: List[PatientRecord]) -> None:
    # Insert benchmarks measure the cost of inserting all selected records
    # into a new empty structure.
    for record in records:
        structure.insert_record(record)


def benchmark_insert(
    structure_class: Any,
    records: List[PatientRecord],
    runs: int = 5,
) -> Tuple[float, int]:
    timings: List[float] = []
    memory_peaks: List[int] = []

    for _ in range(runs):
        structure = structure_class()
        elapsed_seconds, peak_memory = measure_operation(
            lambda: run_insert_operation(structure, records)
        )
        timings.append(elapsed_seconds)
        memory_peaks.append(peak_memory)

    return statistics.mean(timings), int(statistics.mean(memory_peaks))


def benchmark_search(
    structure_class: Any,
    records: List[PatientRecord],
    search_id: int,
    runs: int = 5,
) -> Tuple[float, int]:
    timings: List[float] = []
    memory_peaks: List[int] = []

    for _ in range(runs):
        structure = build_structure(structure_class(), records)
        elapsed_seconds, peak_memory = measure_operation(
            lambda: structure.search_record(search_id)
        )
        timings.append(elapsed_seconds)
        memory_peaks.append(peak_memory)

    return statistics.mean(timings), int(statistics.mean(memory_peaks))


def benchmark_delete(
    structure_class: Any,
    records: List[PatientRecord],
    delete_id: int,
    runs: int = 5,
) -> Tuple[float, int]:
    timings: List[float] = []
    memory_peaks: List[int] = []

    for _ in range(runs):
        structure = build_structure(structure_class(), records)
        elapsed_seconds, peak_memory = measure_operation(
            lambda: structure.delete_record(delete_id)
        )
        timings.append(elapsed_seconds)
        memory_peaks.append(peak_memory)

    return statistics.mean(timings), int(statistics.mean(memory_peaks))


def benchmark_traverse(
    structure_class: Any,
    records: List[PatientRecord],
    runs: int = 5,
) -> Tuple[float, int]:
    timings: List[float] = []
    memory_peaks: List[int] = []

    for _ in range(runs):
        structure = build_structure(structure_class(), records)
        elapsed_seconds, peak_memory = measure_operation(structure.traverse_records)
        timings.append(elapsed_seconds)
        memory_peaks.append(peak_memory)

    return statistics.mean(timings), int(statistics.mean(memory_peaks))


def run_selected_benchmark(
    structure_name: str,
    structure_class: Any,
    operation_name: str,
    records: List[PatientRecord],
    runs: int = 5,
) -> BenchmarkResult:
    # This dispatcher routes the user's selection to the correct benchmark.
    if not records:
        raise ValueError("At least one record is required for benchmarking.")

    operations: Dict[str, Callable[[], Tuple[float, int]]] = {
        "insert": lambda: benchmark_insert(structure_class, records, runs),
        "search": lambda: benchmark_search(
            structure_class,
            records,
            records[len(records) // 2].id,
            runs,
        ),
        "delete": lambda: benchmark_delete(
            structure_class,
            records,
            records[-1].id,
            runs,
        ),
        "traverse": lambda: benchmark_traverse(structure_class, records, runs),
    }

    if operation_name not in operations:
        raise ValueError(f"Unsupported operation: {operation_name}")

    average_seconds, average_peak_memory_bytes = operations[operation_name]()
    complexity = OPERATION_COMPLEXITIES[structure_name][operation_name]

    return BenchmarkResult(
        structure_name=structure_name,
        operation_name=operation_name,
        record_count=len(records),
        runs=runs,
        average_seconds=average_seconds,
        average_peak_memory_bytes=average_peak_memory_bytes,
        time_complexity=complexity,
    )


def run_all_structures_summary(
    structures: Dict[str, Any],
    records: List[PatientRecord],
    runs: int = 5,
) -> Dict[str, Dict[str, BenchmarkResult]]:
    # This function builds the comparison table across all structures.
    if not records:
        raise ValueError("At least one record is required for benchmarking.")

    operations = ["insert", "search", "delete", "traverse"]
    summary: Dict[str, Dict[str, BenchmarkResult]] = {}

    for structure_name, structure_class in structures.items():
        summary[structure_name] = {}

        for operation_name in operations:
            summary[structure_name][operation_name] = run_selected_benchmark(
                structure_name=structure_name,
                structure_class=structure_class,
                operation_name=operation_name,
                records=records,
                runs=runs,
            )

    return summary
